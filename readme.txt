The aim of this project is to create a 'process in the cloud' set of tools for audio mastering.

First step is a proof of concept.
  -Import audio of more than one person talking
  -Identify each person 
  -Apply a different gain level to each person


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


Notes on how the program will work
  -On the client side
    -Audio files can be uploaded
    -Tools (functions) can be added and dragged around
    -Input files are connected to the tools in the desired order
    -Output icons are connected at the end of a chain
    -Final output can be downloaded

  -On the Server side
    -Uploaded files become tracks
    -Multi track files become groups
    -As changes are made on the client side, update output audio track
    -The output of every function becomes a new track (or group)
    -Only make updates to the required tracks
    -Stream audio to user when able so user is able to hear changes as soon as possible

