def parse_command(comment: str):
    comment = comment.strip()
    if not comment.startswith('/'):
        return None, None
    parts = comment[1:].split(None, 1)
    command = parts[0]
    arguments = parts[1] if len(parts) > 1 else ""
    return command, arguments.strip()