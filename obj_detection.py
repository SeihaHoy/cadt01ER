import json
import cv2, math
from realsense_depth import *
from object_detection.load_frozen import *
import log_msg.logger as log
import motors.motor_handlers as mm

# Initialize Camera Intel Realsense
dc = DepthCamera()
intr = dc.get_camera_intrinsics()
theta=0

# Initialize Tensorflow
dt = MyDectector()

window_name = "CADT's Robocon"
cv2.namedWindow(window_name, cv2.WINDOW_AUTOSIZE)

def detect_object(verts, depth_frame, color_image):
    image_expanded = np.expand_dims(color_image, axis=0)
    (boxes, scores, classes, num) = dt.sess.run([dt.detection_boxes, dt.detection_scores, dt.detection_classes, dt.num_detections], 
    feed_dict={dt.image_tensor: image_expanded})

    boxes = np.squeeze(boxes)
    classes = np.squeeze(classes).astype(np.int32)
    scores = np.squeeze(scores)

    results = []
    
    for idx in range (int(num)):
        class_ = classes[idx]
        score = scores[idx]
        box = boxes[idx]

        if score > 0.8 and class_ == 1:
            left = box[1] * dc.W
            top = box[0] * dc.H
            right = box[3] * dc.W
            bottom = box[2] * dc.H
            width = right - left
            height = bottom - top

            bbox = (int(left), int(top), int(width), int(height))

            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))



            # cv2.rectangle(color_image, p1, p2, (0, 255 ,0 ), 2, 1)
            # cv2.putText(color_image, "#{}".format(idx), (int(bbox[0]), int(bbox[1]) - 10), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255))

            height = real_world_height(color_image, bbox, verts)
            mid_pt = (int(bbox[0] + bbox[2] / 2), int(bbox[1] + bbox[3] / 2))
            # Calculate real world coordinates
            Xtarget, Ytarget, Ztarget = real_world_coordinate(depth_frame, mid_pt)
            if (Ztarget == 0):
                continue

            X = float("{:.2f}".format(Xtarget))
            Y = float("{:.2f}".format(Ytarget))
            Z = float("{:.2f}".format(Ztarget))

            # gbr = None
            # try:
            #     gbr = {color_image[int(mid_pt[0]), int(mid_pt[1])]}
            # except:
            #     print(f"GBR type {type(color_image[int(100), int(100)])}")

            # find error 

            error_y = int(dc.H/2) - int((p1[1]+p2[1])/2)
            error_x = int(dc.W/2) - int((p1[0]+p2[0])/2)

            results.append({
                "id": int(idx),
                "class": int(class_),
                "score": int(score),
                "x": X,
                "y": Y,
                "z": Z,
                "height": height,
                "ptx": int(mid_pt[0]),
                "pty": int(mid_pt[1]),
                "p1" : p1,
                "p2": p2,
                "errorX": error_x
            })

            cv2.putText(color_image, f"{error_x} , {error_y}", (int(mid_pt[0] + 10), int(mid_pt[1] + 20)),cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255))

            coordinates_text = "(x=" + str(X) + \
                               ", y=" + str(Y) + \
                               ", z=" + str(Z) + ")"
            print(f"[INFO] Detected {idx} from {Z}mm away, height {height}m @ {coordinates_text}.")

            # global EnableImgShow
            # if EnableImgShow:
            cv2.line(color_image, (int((p1[0]+p2[0])/2),int((p1[1]+p2[1])/2) ), (320, 240), (255,0,0), 2) 
            cv2.circle(color_image, mid_pt, 4, (0, 0, 255))
            cv2.putText(color_image, f"{Z/1000}m @ {coordinates_text}", (int(mid_pt[0] + 10), int(mid_pt[1])),
                        cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255))

    return results

def find_ball(results, color_image):
    dis_y = []
    dis_y_arr = []
    if len(results):
        for ball in (results):
            h= ball["pty"] - 320
            dis_y.append({
                "id_ball": ball["id"], 
                "dis_y": h,
                "p1": ball["p1"],
                "p2": ball["p2"],
                "errorX": ball["errorX"]
                })
            dis_y_arr.append(h)
            # print(f"ball {ball}")

            # dis_y.append(h)
        
        max_y = min(dis_y_arr)
        for i in dis_y:
            if i["dis_y"] == max_y:
                print(f"results : {i}")
                cv2.rectangle(color_image, i["p1"], i["p2"], (0, 255 ,0 ), 2, 1)
                deg = 0
                if i["errorX"] < 0:
                    #Left
                    deg = translate(i["errorX"], 0, -320, 0, 60)

                elif i["errorX"] > 0:
                    #Right
                    deg = translate(i["errorX"], 0, 320, -60, 0)
                    
                
                print("Deg: {}".format(deg))
                mm.runmotorspeed(1, deg, 180)
                break

def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)


             

def real_world_height(color_image, bbox, verts):
    p1 = (int(bbox[0]), int(bbox[1]))
    p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
    # x,y,z of bounding box
    obj_points = verts[int(bbox[1]):int(bbox[1] + bbox[3]), int(bbox[0]):int(bbox[0] + bbox[2])].reshape(-1, 3)
    zs = obj_points[:, 2]

    z = np.median(zs)

    ys = obj_points[:, 1]
    ys = np.delete(ys, np.where((zs < z - 1) | (zs > z + 1)))  # take only y for close z to prevent including background

    my = np.amin(ys, initial=1)
    My = np.amax(ys, initial=-1)

    height = (My - my)  # add next to rectangle print of height using cv library
    height = float("{:.2f}".format(height))

    # Write some Text
    # global EnableImgShow
    # if EnableImgShow:
    height_txt = str(height) + "m"
    font = cv2.FONT_HERSHEY_SIMPLEX
    bottomLeftCornerOfText = (p1[0], p1[1] + 20)
    fontScale = 1
    fontColor = (255, 255, 255)
    lineType = 2
    cv2.putText(color_image, height_txt,
                bottomLeftCornerOfText,
                font,
                fontScale,
                fontColor,
                lineType)
    return height
# test
def real_world_coordinate(depth_frame, img_point):
    # See https://www.youtube.com/watch?v=--81OoXMvlw
    distance = depth_frame.get_distance(img_point[0], img_point[1]) * 1000  # convert to mm
    xTemp = distance * (img_point[0] - intr.ppx) / intr.fx
    yTemp = distance * (img_point[1] - intr.ppy) / intr.fy
    zTemp = distance

    Xtarget = xTemp - 35  # 35 is RGB camera module offset from the center of the realsense
    Ytarget = -(zTemp * math.sin(theta) + yTemp * math.cos(theta))
    Ztarget = zTemp * math.cos(theta) + yTemp * math.sin(theta)

    # Actually, Ztarget is distance

    return Xtarget, Ytarget, Ztarget


def get_frame():
    points, depth_frame, color_frame = dc.get_frame()

    # depth_image = np.asanyarray(depth_frame.get_data())

    # visualize the depth map captured by the RealSense camera
    # colorizer = rs.colorizer()
    # colorized_depth = np.asanyarray(colorizer.colorize(depth_frame).get_data())

    color_data = color_frame.get_data()
    # visualize color image
    color_image = np.asanyarray(color_data)

    verts = np.asanyarray(points.get_vertices()).view(np.float32).reshape(-1, dc.W, 3)  # xyz
    cv2.line(color_image, (320 , 0), (320, 480), (0,0,255), 1) 
    cv2.line(color_image, (0 , 240), (640, 240), (0,0,255), 1) 
    # Detect image using opencv
    results = detect_object(verts, depth_frame, color_image)
    
    find_ball(results, color_image)
    
    print(f"Detected result per frame: {len(results)}")
    for rs in results:
        print(f"==> Detected {rs['id']} at ({rs['x']}, {rs['y']}, {rs['z']}), height {rs['height']}m")

    # global EnableImgShow
    # if EnableImgShow:
    # Image show
    # cv2.imshow("depth frame", colorized_depth)
    # cv2.imshow(windowName, color_image)
    # cv2.imshow(window_name, color_image)

    return (results, color_image, color_data)


def release():
    dc.release()
    log.info("[DETECTION] Released.")


# Get first frame to initialize tf calculation
get_frame()

# if __name__ == "__main__":
    # while True:
    #     (detected, img, color_data) = get_frame()
    #     # if len(detected) > 0:
    #         # Write latest results into file
    #         # f = open('__detected.txt', 'wb')
    #         # pickle.dump(detected, f)
    #         #f.write(pickle.dumps(detected).decode("utf-8"))
    #         # f.close()
    #     key = cv2.waitKey(1)  # 0 for waiting key pressed, 1 for waiting every 1ms
    #     if key == 27:  # Esc key
    #         # Write latest result into file
    #         log.info("Write data to __detected.txt")
    #         f = open('__detected.txt', 'w')
    #         f.write(json.dumps(detected))
    #         f.close()

    #         log.info("Write image to __detected_img.png")
    #         cv2.imwrite('__detected_img1.png', img)

    #         cv2.destroyAllWindows()
    #         release()
    #         break