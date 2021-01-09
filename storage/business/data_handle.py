

def receive(data):
    return json.loads(data)

stock_info_json_parsed = receive(data)

stock_info_json_parsed["stock_info_id"] = extract_stock_id(stock_info_json_parsed["ts_code"])