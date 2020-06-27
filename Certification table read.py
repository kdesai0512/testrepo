from knackpy import Knack

filters = {
    'match': 'and',
      'rules': [
        {
          'field':'field_208',
          'operator':'is',
          'value':'06/27/2020'
        },
        {
          'field':'field_148',
          'operator':'is',
          'value':'Complete'
        }
      ]
    }

kn = Knack(
    obj = 'object_17',
    app_id = '5ee26710da32c300153905ca',
    api_key = 'abde5d40-ae8d-11ea-8cd1-1dc626a4204b',
    filters=filters
    )
for row in kn.data:
        print(row)

kn.to_csv('c:\data\cert.csv')
