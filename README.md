* Currently supported Attachments are:
  1. card = for buttons with payload/url
  2. text = for simple text
  3. dropdown = for quick reply

* Currently supported Data Nodes are:
  - Response
  - Prompt
  - Handoff


Workflow Builder in BotPress rules to follow:
---------------------------------------------
There are 3 types of tabs for a node in botpress worflow
  1. onEnter - only for HandOff nodes
  2. onReceive - for Prompt and Response nodes
  3. Transitions :
    - based on 'quick reply values' (used in 2nd point) which node to go next.
    - If we want trasition based on a value then put that value ONLY in 'Raw Expression (advanced) ' field
    - If we want trasition no matter what user gives input then select 'Always'


Process to run script to generate AI Studio based JSON:
-------------------------------------------------------
1. Put 'scripts' folder inside downloaded botpress folder 
    (i.e. botpress-v12_15_2-darwin-x64)
2. Go to script folder & run following commond in terminal ->    python app.py
   