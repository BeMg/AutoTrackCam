# AutoTrackCam

## Goal

Create a Auto Track object WebCam for recording in class or speech

## Implement

- GetVideoFromCam
- DetectPeople
    - DetectFace
    - DetectBody
- DetectScreen
- TurnCam

## Detail

### GetVideoFromCam

By Device or file to Get Frame.

- input: device number or video path
- output: a object which can divide video to frame

### DetectPeople

Use multiple object Detecion method to Detect object from frame

- input: frame
- output: rect which invovle People, maybe face or anyelse.

### DetectScreen

Find the white Screen by theshold method

- input: frame need find screen
- output: rect where screen in

### TurnCam

Turn WebCam by Raspberry Pi

- input: step, and direction
- output: none, Just Turn Cam