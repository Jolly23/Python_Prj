#!/usr/bin/python
# coding=utf-8
from CetTicket import CetTicket, TicketNotFound


def getTicket(temp_province=None, temp_school=None, temp_name=None, temp_cet=None):
	province = temp_province
	school = temp_school
	name = temp_name
	cet = temp_cet
	result = dict(error=False)
	try:
		result['ticket_number']=CetTicket.find_ticket_number(province,school,name,cet_type=cet)
	except TicketNotFound:
		result['error'] = True
	return result


def get_DLNU_Score(temp_name=None, temp_cet=None):
	province = u'辽宁'
	school = u'大连民族大学'
	name = temp_name
	cet=temp_cet
	result = getTicket(province, school, name, cet)
	if (result["error"]):
		return result
	ticket=result['ticket_number']
	return getScore(ticket, name)


a = get_DLNU_Score(u'闫霄')
print a