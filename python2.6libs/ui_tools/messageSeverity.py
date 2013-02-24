'''Acts as an enum of severity levels

Safer severities (i.e. Message, ImportantMessage) are equal to non-negative 
integers. Less safe severities (i.e. Warning, Error, Fatal) are equal to 
negative integers.'''

Message = 0
ImportantMessage = 1
Warning = -1
Error = -2
Fatal = -3

