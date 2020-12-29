#!/usr/bin/env python
"""app.py: JSON Generator script for AI Studio using open-source BotPress studio."""
__author__      = "Tushar Soni"
__email__ = "tushar@netomi.com"


import json, copy, os.path, sys
from collections import OrderedDict
from pprint import pprint



# bot info
intent_key = raw_input("Enter your Intent Key (of netomi) : ").strip()
netomi_bot_id = raw_input("Enter your BotID (of netomi) : ").strip()
botpress_bot_id = raw_input("Enter your BotID (of botpress) : ").strip()

bot_dir = '../data/bots/'+botpress_bot_id
if os.path.isdir(bot_dir) is False:
  sys.exit("\nError: BotID '" + botpress_bot_id + "' not found in BotPress, please enter correct & exact BotID!\n")

content_dir = bot_dir + '/content-elements/'

##################################################################################

print("\nGenerating JSON for AI Studio...")
# create map of all data nodes of all types (card, text, quick reply)
elements_map = {}

# read botpress generated jsons
# read card json and put nodes in elements_map
try:
  card_file_name = content_dir + 'builtin_card.json'
  with open(card_file_name) as card_file:
    card_json = json.load(card_file, object_pairs_hook=OrderedDict)

  for node in card_json:
    elements_map[node['id']] = node
except:
  pass

# read text json and put nodes in elements_map
try:
  text_file_name = content_dir + 'builtin_text.json'
  with open(text_file_name) as text_file:
    text_json = json.load(text_file, object_pairs_hook=OrderedDict)

  for node in text_json:
    elements_map[node['id']] = node
except:
  pass

# read quick reply json and put nodes in elements_map
try:
  quick_reply_file_name = content_dir + 'dropdown.json'
  with open(quick_reply_file_name) as quk_rply_file:
    quick_reply_json = json.load(quk_rply_file, object_pairs_hook=OrderedDict)

  for node in quick_reply_json:
    elements_map[node['id']] = node
except:
  pass

# read tranition flow json
flow_file_name = bot_dir + '/flows/main.flow.json'
with open(flow_file_name) as flow_file:
  flow_json = json.load(flow_file, object_pairs_hook=OrderedDict)

##################################################################################

#read netomi reference jsons

#read quick reply option node json
qreply_option_node_file = open('references/qreply-option.json')
qreply_option_node_json = json.load(qreply_option_node_file, object_pairs_hook=OrderedDict)

#read quick reply node json
quick_reply_node_file = open('references/quick-reply.json')
quick_reply_node_json = json.load(quick_reply_node_file, object_pairs_hook=OrderedDict)

#read button postback node json
button_postback_node_file = open('references/button-postback.json')
button_postback_node_json = json.load(button_postback_node_file, object_pairs_hook=OrderedDict)

#read button url node json
button_url_node_file = open('references/button-url.json')
button_url_node_json = json.load(button_url_node_file, object_pairs_hook=OrderedDict)

#read card node json
card_node_file = open('references/card-node.json')
card_node_json = json.load(card_node_file, object_pairs_hook=OrderedDict)

#read text data json
text_node_file = open('references/text-node.json')
text_node_json = json.load(text_node_file, object_pairs_hook=OrderedDict)

#read prompt json
prompt_file = open('references/chat-prompt.json')
prompt_json = json.load(prompt_file, object_pairs_hook=OrderedDict)

#read response json
response_file = open('references/chat-response.json')
response_json = json.load(response_file, object_pairs_hook=OrderedDict)

#read entity json
entity_file = open('references/entity.json')
entity_json = json.load(entity_file, object_pairs_hook=OrderedDict)

#read transition json
transition_file = open('references/transition.json')
transition_json = json.load(transition_file, object_pairs_hook=OrderedDict)

#read handoff json
handoff_file = open('references/handoff.json')
handoff_json = json.load(handoff_file, object_pairs_hook=OrderedDict)

#read handoff json
skeleton_file = open('references/skeleton.json')
skeleton_json = json.load(skeleton_file, object_pairs_hook=OrderedDict)

##################################################################################

# preprocess common fields
skeleton_json['flowEntityMap']['INTENT_TYPE']['botId'] = netomi_bot_id
skeleton_json['flowEntityMap']['EMAIL_ID']['botId'] = netomi_bot_id
skeleton_json['name'] = intent_key


def create_options(actions):
  options = []
  for action in actions:
    qreply_option_node = qreply_option_node_json
    qreply_option_node['label'] = action['label'].strip()
    qreply_option_node['description'] = action['label'].strip()
    qreply_option_node['metadata'] = action['value'].strip()
    options.append(copy.deepcopy(qreply_option_node))
  
  return options

def create_quick_reply(data):
  quick_reply_node = quick_reply_node_json
  quick_reply_node['text'] = data['message$en']
  quick_reply_node['quickReply']['options'] = create_options(data['options$en'])
  return quick_reply_node

def create_buttons(actions):
  buttons = []
  for action in actions:
    if action['action'] == 'Postback':
      button_postback_node = button_postback_node_json
      button_postback_node['title'] = action['title'].strip()
      button_postback_node['payload'] = action['payload'].strip()
      buttons.append(copy.deepcopy(button_postback_node))
    elif action['action'] == 'Open URL':
      button_url_node = button_url_node_json
      button_url_node['title'] = action['title'].strip()
      button_url_node['url'] = action['url'].strip()
      buttons.append(copy.deepcopy(button_url_node))
    
  return buttons

def create_card(data):
  card_node = card_node_json
  card_node['text'] = data['title$en'].strip()
  card_node['buttons'] = create_buttons(data['actions$en'])
  return card_node

def create_text(text_data):
  text_node = text_node_json
  text_node['text'] = text_data
  return text_node

def create_attachements(content_ids):
  attachments = []
  for data_id in content_ids:
    data_id = data_id.replace('say #!', '')

    if data_id.find('text') != -1:
      text_node = create_text(elements_map[data_id]['formData']['text$en'])
      attachments.append(copy.deepcopy(text_node))
    elif data_id.find('card') != -1:
      card_node = create_card(elements_map[data_id]['formData'])
      attachments.append(copy.deepcopy(card_node))
    elif data_id.find('dropdown') != -1:  # quickreply
      quick_reply_node = create_quick_reply(elements_map[data_id]['formData'])
      attachments.append(copy.deepcopy(quick_reply_node))
    else:
      print('Invalid attachment for id: ' + data_id)
  
  return attachments

def create_response(node):
  response_node = response_json
  node['name'] = node['name'].upper()
  response_node['label'] = node['name']
  response_node['name'] = node['name']

  if node['id'] == 'entry':
    response_node['level'] = 'START'
  else:
    response_node['level'] = 'TERMINATE'
  
  attachments = create_attachements(node['onReceive'])
  response_node['response']['contextResponses'][0]['localeResponsesMap']['default'][0]['responseUnits'][0]['attachments'] = attachments
  return response_node

def create_prompt(node, entity_name):
  prompt_node = prompt_json
  node['name'] = node['name'].upper()
  prompt_node['label'] = node['name']
  prompt_node['name'] = node['name']
  prompt_node['response']['label'] = node['name']
  prompt_node['response']['name'] = node['name']
  prompt_node['response']['entities'][0]['name'] = entity_name

  if node['id'] == 'entry':
    prompt_node['level'] = 'START'
  else:
    prompt_node['level'] = 'INTERMEDIATE'

  attachments = create_attachements(node['onReceive'])
  prompt_node['response']['response']['contextResponses'][0]['localeResponsesMap']['default'][0]['responseUnits'][0]['attachments'] = attachments
  prompt_node['response']['retryAction']['contextResponses'][0]['localeResponsesMap']['default'][0]['responseUnits'][0]['attachments'] = attachments

  return prompt_node

def create_handoff(node):
  handoff_node = handoff_json
  node['name'] = node['name'].upper()
  handoff_node['label'] = node['name']
  handoff_node['name'] = node['name']
  
  if node['id'] == 'entry':
    handoff_node['level'] = 'START'
  else:
    handoff_node['level'] = 'TERMINATE'

  attachments = create_attachements(node['onEnter'])
  handoff_node['response']['standardActionResponse']['contextResponses'][0]['localeResponsesMap']['default'][0]['responseUnits'][0]['attachments'] = attachments
  return handoff_node

def append_data_node(data_node):
  skeleton_json['nodes'].append(copy.deepcopy(data_node))

def create_transition(start_node_name, entity_name, target_node_name, condition_value):
  transition_node = transition_json
  transition_node['sourceNodeId'] = start_node_name.upper()
  transition_node['targetNodeId'] = target_node_name.upper()
  entity_value = entity_name + "_value"
  if condition_value == 'true':
    transition_node['guardMetaData']['rule']['expression'] = entity_value + " != null"
  else:
    transition_node['guardMetaData']['rule']['expression'] = entity_value + " != null && " + entity_value + ".equalsIgnoreCase('" + condition_value + "')"
  transition_node['guardMetaData']['rule']['expectedAttributes'][0]['name'] = entity_name
  return transition_node

def append_transition_node(transition_node):
  skeleton_json['transitions'].append(copy.deepcopy(transition_node))

def create_entity(entity_name):
  entity_node = entity_json
  entity_node[entity_name] = entity_node['ORDER_ID']
  entity_node[entity_name]['id'] = entity_name
  entity_node[entity_name]['botId'] = netomi_bot_id
  entity_node[entity_name]['name'] = entity_name
  entity_node[entity_name]['className'] = entity_name
  entity_node[entity_name]['label'] = entity_name
  entity_node[entity_name]['description'] = entity_name
  return entity_node[entity_name]

def append_entity_node(entity_node, entity_name):
  skeleton_json['flowEntityMap'].__setitem__(copy.copy(entity_name), copy.deepcopy(entity_node))


##################################################################################

# process tranistions main flow
for node in flow_json['nodes']:
  node['name'] = node['name'].strip().upper()
  entity_name = node['name']+ '_ENTITY'

  #create data node
  data_node = None
  if not node['next']:
    if node['onReceive'] is not None:
      data_node = create_response(node)
    elif node['onEnter'] is not None and len(node['onEnter']) > 0:
      data_node = create_handoff(node)
  elif node['onReceive'] is not None:
    data_node = create_prompt(node, entity_name)
    #create entity for prompt
    append_entity_node(create_entity(entity_name), entity_name)

  if data_node is not None:
    append_data_node(data_node)
  else:
    print('Data node: ' + node['name'] + ' is not supported (only Response/Prompt/Handoff works)')

  #create transition node
  for next_node in node['next']:
    append_transition_node(create_transition(node['name'].strip(), entity_name, next_node['node'].strip(), next_node['condition'].strip()))


##################################################################################

#print output json
print("Successfully generated JSON for AI Studio!")
print('\n\n**************************** | JSON Output | ****************************\n\n')
print(json.dumps(skeleton_json, ensure_ascii=False))