@simple_slack_bot.register("message")
def roll_callback(request):
    """This function is called every time a message is sent to a channel out Bot is in
    :param request: the SlackRequest we receive along with the event. See the README.md for full documentation
    :return: None
    """
    fields = []

    if "CBGJ4P2JJ" != request.channel:
        return

    if request.type != "message":
        return

    # player message
    if request._slack_event.event.get("subtype") == "me_message":
            fields.append("Player")
            fields.append(get_user(request.user))
            fields.append(request.message)

    # DM message
    elif request.message.startswith("&gt;"):
            fields.append("DM")
            fields.append(get_user(request.user))
            fields.append(request.message)

    if fields:
        with open(r"transcript.csv", 'a') as transcript:
            writer = csv.writer(transcript)
            writer.writerow(fields)
