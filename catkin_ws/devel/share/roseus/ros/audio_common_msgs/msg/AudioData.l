;; Auto-generated. Do not edit!


(when (boundp 'audio_common_msgs::AudioData)
  (if (not (find-package "AUDIO_COMMON_MSGS"))
    (make-package "AUDIO_COMMON_MSGS"))
  (shadow 'AudioData (find-package "AUDIO_COMMON_MSGS")))
(unless (find-package "AUDIO_COMMON_MSGS::AUDIODATA")
  (make-package "AUDIO_COMMON_MSGS::AUDIODATA"))

(in-package "ROS")
;;//! \htmlinclude AudioData.msg.html


(defclass audio_common_msgs::AudioData
  :super ros::object
  :slots (_data ))

(defmethod audio_common_msgs::AudioData
  (:init
   (&key
    ((:data __data) (make-array 0 :initial-element 0 :element-type :integer))
    )
   (send-super :init)
   (setq _data __data)
   self)
  (:data
   (&optional __data)
   (if __data (setq _data __data)) _data)
  (:serialization-length
   ()
   (+
    ;; int16[] _data
    (* 2    (length _data)) 4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; int16[] _data
     (write-long (length _data) s)
     (dotimes (i (length _data))
       (write-word (elt _data i) s)
       )
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; int16[] _data
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _data (instantiate integer-vector n))
     (dotimes (i n)
     (setf (elt _data i) (sys::peek buf ptr- :short)) (incf ptr- 2)
     ))
   ;;
   self)
  )

(setf (get audio_common_msgs::AudioData :md5sum-) "8560fbebb34fa1b9472337b5c3d38fda")
(setf (get audio_common_msgs::AudioData :datatype-) "audio_common_msgs/AudioData")
(setf (get audio_common_msgs::AudioData :definition-)
      "int16[] data

")



(provide :audio_common_msgs/AudioData "8560fbebb34fa1b9472337b5c3d38fda")


