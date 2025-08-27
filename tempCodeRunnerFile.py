 buffer = io.BytesIO()
    buffer.write(report.encode("utf-8"))
    buffer.seek(0)
    return send_file(
        buffer,
        as_attachment=True,
        download_name="chatbot_profile.txt",
        mimetype="text/plain"