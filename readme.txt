The aim of this project is to create a 'process in the cloud' set of tools for audio mastering.

Expected user experience
  -Upload audio files
  -In a node based GUI, connect filters and effects to audio tracks
  -Listen to the edited audio as changes are made to settings
    -Audio is streamed from the server
  -Download modified audio files

------------------------------------------------------------------------------------------------

First step is a proof of concept.
  -Import audio of more than one person talking
  -Identify each person 
  -Apply a different gain level to each person

------------------------------------------------------------------------------------------------

Notes on how the program will work
  -Main data structure is the 'track' (or groups of multiple tracks)
    -Uploaded files become tracks
    -Tracks that should be processed together (eg stereo tracks) are put in a 'group'
  -'Commands' take various input, then output a track (or group)
  -'Commands' are joined together to process the audio as required
  -All data is referred to using identifiers
  -The server processes the audio as required

------------------------------------------------------------------------------------------------

Notes on data structure
  -All data is based around 4 structures
    -Track
    -Group
    -[Function Settings]
    -[Processed Samples]

  -Track
    -Works around a 'getValue(time)' function
    -Can store data in any required format, even as an equation of other tracks
    -Relevant MetaData is stored in a dictionary
    -Every track has a unique ID, derived from the function (and arguments) that created it

  -Group
    -Can contain a number of tracks and other groups
    -Relevant MetaData is stored in a dictionary

  -[Function Settings]
    -A dictionary of settings that control the behaviour of a function
    -For example, a list of names to auto assign to tracks in a group

  -[Processed Samples]
    -A structured set of data required by a function
    -For example, vocal characteristics of several people

------------------------------------------------------------------------------------------------
