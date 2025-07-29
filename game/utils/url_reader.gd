extends Node
class_name URLReader


static func read_params() -> Dictionary:
    var url = JavaScriptBridge.eval("window.location.href", true)
    if url is String:
        var result = {}
        var query_index = url.find("?")
        if query_index == -1:
            return result
        var query = url.substr(query_index + 1)
        for pair in query.split("&"):
            var parts = pair.split("=")
            if parts.size() == 2:
                var key = parts[0]
                var value = parts[1]
                result[key] = value
        return result
    else:
        return {}