class Emojis:
    # General
    ROCKET = '<tg-emoji emoji-id="6129639980387015660">🚀</tg-emoji>'
    CHECK = '<tg-emoji emoji-id="6266787022111773140">✅</tg-emoji>'
    CROSS = '<tg-emoji emoji-id="6179128006615765757">❌</tg-emoji>'
    WARNING = '<tg-emoji emoji-id="6118652646589993726">⚠️</tg-emoji>'
    EYE = '<tg-emoji emoji-id="5426900601101374618">🧿</tg-emoji>'
    STATS = '<tg-emoji emoji-id="6170421210258609322">📊</tg-emoji>'
    TOOLS = '<tg-emoji emoji-id="5462921117423384478">🛠</tg-emoji>'
    BROADCAST = '<tg-emoji emoji-id="6267129592998270736">📣</tg-emoji>'
    LIGHTNING = '<tg-emoji emoji-id="6170464829946468179">⚡️</tg-emoji>'
    
    # Account & Credits
    USER = '<tg-emoji emoji-id="5373012449597335010">👤</tg-emoji>'
    USERS = '<tg-emoji emoji-id="5372926953978341366">👥</tg-emoji>'
    ID = "🆔"
    TICKET = '<tg-emoji emoji-id="5418010521309815154">🎫</tg-emoji>'
    FOLDER = "📑"
    CARD = '<tg-emoji emoji-id="5472250091332993630">💳</tg-emoji>'
    LINK = '<tg-emoji emoji-id="5375129357373165375">🔗</tg-emoji>'
    COOL = '<tg-emoji emoji-id="6276027631364216180">😎</tg-emoji>'
    KING = "🫅"
    DIAMOND = '<tg-emoji emoji-id="5971944878815317190">💠</tg-emoji>'
    PRINCE = '<tg-emoji emoji-id="6118691820986701045">🤴</tg-emoji>'
    
    # Features & Notifications
    CAMERA = '<tg-emoji emoji-id="6141162896605843133">📸</tg-emoji>'
    MAP = '<tg-emoji emoji-id="5415803062738504079">🗺</tg-emoji>'
    TRAFFIC_LIGHT = "🚦"
    HAMSA = '<tg-emoji emoji-id="5404451992456156919">🪬</tg-emoji>'
    BULB = '<tg-emoji emoji-id="5262844652964303985">💡</tg-emoji>'
    ROBOT = '<tg-emoji emoji-id="5372981976804366741">🤖</tg-emoji>'
    GLOBE = '<tg-emoji emoji-id="5265196963602656644">🌍</tg-emoji>'
    BACK = '<tg-emoji emoji-id="5253997076169115797">🔙</tg-emoji>'
    CONGRATS = '<tg-emoji emoji-id="5435933711893797296">🎊</tg-emoji>'
    PIN = '<tg-emoji emoji-id="6267172559851099903">📌</tg-emoji>'
    ALIEN = '<tg-emoji emoji-id="5370869711888194012">👾</tg-emoji>'
    LOCK = '<tg-emoji emoji-id="5897604269141398480">🔐</tg-emoji>'
    
    @classmethod
    def b(cls, val):
        """Returns plain character for buttons (strips <tg-emoji> tags)"""
        import re
        if isinstance(val, str) and "<tg-emoji" in val:
            # Extract content between > and <
            match = re.search(r'>(.*?)<', val)
            return match.group(1) if match else val
        return val

    @classmethod
    def get_id(cls, val):
        """Extracts the emoji-id from the <tg-emoji> tag"""
        import re
        if isinstance(val, str) and "emoji-id=" in val:
            match = re.search(r'emoji-id=["\'](\d+)["\']', val)
            return match.group(1) if match else None
        return None


