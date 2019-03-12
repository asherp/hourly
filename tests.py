from hourly.hourly import *


def test_hourly_work():
	work = get_work_commits('.')
	labor, earnings = get_report('.', None, '2018-10-20 13:16:13-04:00', ['d9ec537b36475b565df6b28d0cab6edc3a89f2da'], 'pro bono')

	print(labor)
	print(earnings)