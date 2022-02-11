#  TO DETECT FINGER AND DO SOME ACTIVIY
import cv2
import mediapipe as mp
import smtplib
import pywhatkit as pw
import pyttsx3
import PyPDF2
cap=cv2.VideoCapture(0)
cap.set(3, 1024)  #for width
cap.set(4, 720)   #for height
cap.set(10, 100)  #for clear brightness
mphand=mp.solutions.hands
hands=mphand.Hands()
mpdraw=mp.solutions.drawing_utils
fingerCoordinates=[(8,6),(12,10),(16,14),(20,18)]
thumbCoordinates=(4,2)
while True:
    success,img=cap.read()
    imgrgb=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results=hands.process(imgrgb)
    multihandmarks=results.multi_hand_landmarks
    if multihandmarks:
        handPoints=[]
        for handl in multihandmarks:
            mpdraw.draw_landmarks(img,handl,mphand.HAND_CONNECTIONS)
        for idx,lm in enumerate(handl.landmark):
            h,w,c=img.shape
            cx,cy=int(lm.x*w),int(lm.y*h)
            handPoints.append((cx,cy))
        for point in handPoints:
            cv2.circle(img,point,10,(0,0,255),cv2.FILLED)
        upcount=0
        for coordinate in fingerCoordinates:
            if handPoints[coordinate[0]][1] < handPoints[coordinate[1]][1]:
                upcount+=1
            if handPoints[thumbCoordinates[1]][0] > handPoints[thumbCoordinates[1]][1]:
                upcount+=1
        if upcount == 1:

            sender_email = "jenishmoradiya80@gmail.com"
            receiver_email = input(str("enter receiver email id : "))

            message = input(str("enter message which you want to send : "))
            server = smtplib.SMTP_SSL("smtp.gmail.com", 465)

            server.login(sender_email, "Jenishmoradiya@80")
            print("Login Successfully")
            server.sendmail(sender_email, receiver_email, message)
            print("Email has been sent to " + receiver_email)
            server.quit()

        elif upcount==2:
            pw.sendwhatmsg("+918347497953", "hello world", 10, 8)
        elif upcount==3:
            book = open('eoi.pdf', 'rb')
            pdfReader = PyPDF2.PdfFileReader(book)
            pages = pdfReader.numPages
            print(pages)
            speak = pyttsx3.init()
            for num in range(0, 2):
                page = pdfReader.getPage(num)
                text = page.extractText()
                speak.say(text)
                speak.runAndWait()
    # cv2.waitKey(5)
    if cv2.waitKey(100)==ord('q'):
        break
    cv2.imshow("finger counter", img)