client_config(.ymla)のcolumn_mapから自動的にキーの抽出
Linkから抽出項目なのか、Indivisualから抽出する項目なのか真明確にする必要がある

基本的には.pyは触らずに済ませることができそう。
きちんとreadmeを書かないと忘れそうだけど

.yamlをdict形式に変換（キーをとりながら活用していく）

<list>
1. htmlの取得
2. contentsの抽出
3. c in contentsにて、それぞれの項目を抽出
4. cごとにspreadsheetに転機

<indivisual>
1. htmlの取得
2. それぞれの項目を抽出
3. spreadsheetに転機

```yaml
column_map:
  - key: company
    column: A
    tag: list

  - key: address
    column: B
    tag: indivisual

  - key: status
    column: C
    tag: system
```

↓

```json
{
  "list": {
    "company": "A"
  },
  "indivisual": {
    "address": "B"
  },
    "system": {
      "status": "C"
    }
}
```

-----------------------

## file
- app/
  - spreadsheet/
  - utillities/
  - scraping/
  - logger/
  - yaml/
- module/
  - [GREEN]/
    - source/
      - list.py
      - indivisual.py
    - logic/
      - list.py
      - indivisual.py
- clients/
  - [0000]/
    - config.yaml
- main.py

-----------------------

## list
for input in inputs
  with synch p
    - open url (playwright)
    - search action (playwright)
    for page in pages
      - extract item (playwright)
      - write to spreadsheet (spreadsheet)
      - next action (playwright)

