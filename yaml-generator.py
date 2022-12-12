'''
    Author : Mustafa
    Date   : 08.12.2022
    Aim    : Generate inddex yaml file on GCP Datastore active index list export. 
    Usage  : export indexes via this command ./google-cloud-sdk/bin/gcloud datastore indexes list > path/output.txt
'''

main_path = '/Users'
file_path = main_path + 'output.txt'
output_file_path =  main_path +  'output_indexes.yaml'
file_content = open(file_path, "r")
index_parts = file_content.read().split("state: READY")

yaml_content = '''indexes :
    #LineTemplate#
'''

index_templates = ''

for i in index_parts:
    index_template = '''
- kind: #kind_name#
  properties:
#name_lines##direction_lines# 
    '''
    
    name_templates = ''
    name_template = "  - name: #index_name#"
    direction_templates = ''
    direction_template = "    direction: desc"
    temp_main = ''
    lines = i.split('\n')
    for line in lines:
        divider_fix1 = 'kind: '
        divider_fix2 = 'name: '
        divider_fix3 = '- direction: DESCENDING'
        
        if divider_fix1 in line:
            steps = line.split(divider_fix1)
            temp_main = index_template
            temp_main = temp_main.replace('#kind_name#', steps[1])
        
        if divider_fix2 in line:
            steps = line.split(divider_fix2)
            temp1 = name_template
            temp1 = temp1.replace('#index_name#', steps[1].strip())
            name_templates = name_templates +temp1 + '\n'
            
        if divider_fix3 in line: 
            direction_templates = direction_templates +direction_template
            
    temp_main = temp_main.replace("#name_lines#", name_templates)
    temp_main = temp_main.replace("#direction_lines#", direction_templates)
    index_templates = index_templates + temp_main; 
    
yaml_content = yaml_content.replace('#LineTemplate#', index_templates) 

file_output = open(output_file_path, 'w')
file_output.write(yaml_content)
file_output.close() 
