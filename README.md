# Botpress Script

### Currently supported Attachments are:
  - card = for buttons with payload/url
  - text = for simple text
  - dropdown = for quick reply

### Currently supported Data Nodes are:
  - Response
  - Prompt
  - Handoff


Setup & Process to run script to generate AI Studio based JSON:
-------------------------------------------------------
1. Clone https://github.com/tsmsg/botpress-script.git repo inside botpress folder (i.e. `botpress-v12_15_2-darwin-x64/`) which can be downloaded from https://botpress.com/download
2. Go to cloned `botpress-script` repo & run following commond in terminal -> `python app.py`


Workflow Builder in BotPress rules to follow:
---------------------------------------------
There are 3 types of tabs for a node in botpress worflow
1. onEnter - only for HandOff nodes
2. onReceive - for Prompt and Response nodes
3. Transitions :
    - based on 'quick reply values' (used in 2nd point) which node to go next.
    - If we want trasition based on a value then put that value ONLY in 'Raw Expression (advanced) ' field
    - If we want trasition no matter what user gives input then select 'Always'