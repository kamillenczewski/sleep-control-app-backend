from tools import getArgs
from model import model, data

def generateContent(prompt):
    return model.generate_content(prompt).text

def composePrompt(userName, dateType, latestDate, data):
    return f"""
        Having this data write a funny note about user's latest time schedule.
        You can allude to previous data of user or other user's data.
        Your answer should consist of plain text.
        Write only answer!
        Your asnwer should contain from 1 to 3 sentences.
        Recent {userName}'s date of {dateType}: {latestDate}.
        Different data: {data}.
    """

def execute(username, date_type, latest_date):
    prompt = composePrompt(username, date_type, latest_date, data)
    note = generateContent(prompt)
    return note



def endpoint():
    args, isAnyNull = getArgs(
        names=['username', 'date_type', 'latest_date'], 
    )
    
    if isAnyNull:
        return

    return execute(*args)
