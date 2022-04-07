import cv2
from os import listdir, mkdir
from os.path import exists, isfile, join

all_files = [f for f in listdir("images/pics") if isfile(join("images/pics", f))]
all_files.sort()

folders = [
    'screenshots', 
    'all',
    'gray',
    'edged', 
    'contours', 
    'biggest-contour', 
    'cropped', 
    'wishlist'
]
for folder in folders:
    if not exists(join("images", folder)):
        mkdir(join("images", folder))

std_x = 0
std_y = 0
std_h = 0
std_w = 0
std_i = 0
problematic_images = list()
for i, file_name in enumerate(all_files):
    pic = cv2.imread("images/pics/{}".format(all_files[i]))

    prefix = 100 + i + 1
    cv2.imwrite("images/screenshots/screenshot-{}.jpg".format(prefix), pic)
    screenshot = cv2.imread("images/screenshots/screenshot-{}.jpg".format(prefix))
    
    cv2.imwrite("images/all/{}--01--screenshot-{}.jpg".format(prefix, prefix), screenshot)
    img = cv2.imread("images/all/{}--01--screenshot-{}.jpg".format(prefix, prefix))

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite("images/all/{}--02--gray-{}.jpg".format(prefix, prefix), gray)
    cv2.imwrite("images/gray/screenshot-{}.jpg".format(prefix), gray)

    img_edged = cv2.Canny(gray, 30, 200)
    cv2.imwrite("images/all/{}--03--edged-{}.jpg".format(prefix, prefix), img_edged)
    cv2.imwrite("images/edged/screenshot-{}.jpg".format(prefix), img_edged)

    contours, hierarchy = cv2.findContours(img_edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(img, contours, -1, (0, 255, 0), 3)
    cv2.imwrite("images/all/{}--04--contours-{}.jpg".format(prefix, prefix), img)
    cv2.imwrite("images/contours/screenshot-{}.jpg".format(prefix), img)

    c = max(contours, key = cv2.contourArea)
    x,y,w,h = cv2.boundingRect(c)
    cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255), 3)
    cv2.imwrite("images/all/{}--05--biggest-contour-{}.jpg".format(prefix, prefix), img)
    cv2.imwrite("images/biggest-contour/screenshot-{}.jpg".format(prefix), img)
    
    if i == 0:
        std_h = h
        std_w = w
    else:
        problematic = False
        if abs(w - std_w) / std_w > 0.1:
            problematic = True
        
        if abs(h - std_h) / std_h > 0.1:
            problematic = True
            
        if problematic:
            problematic_images.append(i)
            cropped_screenshot = screenshot[y:y+h, x:x+w]
            cv2.imwrite("images/all/{}--06--problematic-cropped-{}.jpg".format(prefix, prefix), cropped_screenshot)
            cv2.imwrite("images/cropped/screenshot-{}.jpg".format(prefix), cropped_screenshot)
            continue
        
        if std_i == 0:
            std_h = h
            std_w = w
            std_x = x
            std_y = y
            std_i = i
                
    cropped_screenshot = screenshot[y:y+h, x:x+w]
    cv2.imwrite("images/all/{}--06--correct-cropped-{}.jpg".format(prefix, prefix), cropped_screenshot)
    cv2.imwrite("images/cropped/screenshot-{}.jpg".format(prefix), cropped_screenshot)
    cv2.imwrite("images/wishlist/item-{}.jpg".format(prefix), cropped_screenshot)
                
for i in problematic_images:
    prefix = 100 + i + 1
    screenshot = cv2.imread("images/screenshots/screenshot-{}.jpg".format(prefix))
    cropped_screenshot = screenshot[std_y:std_y+std_h, std_x:std_x+std_w]
    cv2.imwrite("images/all/{}--07--correct-cropped-{}.jpg".format(prefix, prefix), cropped_screenshot)
    cv2.imwrite("images/wishlist/item-{}.jpg".format(prefix), cropped_screenshot)