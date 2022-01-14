#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:yang wei
@file:ai_result_orm.py
@time:2021/10/27
"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, INT, TIMESTAMP

from cyclone.utils.save_db import SaveDB

Base = declarative_base()


class AiReport(Base):
    __tablename__ = 'test_report'

    id = Column(Integer, primary_key=True)
    failed = Column(INT)
    broken = Column(INT)
    skipped = Column(INT)
    passed = Column(INT)
    unknown = Column(INT)
    total = Column(INT)
    start = Column(TIMESTAMP)
    stop = Column(TIMESTAMP)
    duration = Column(Integer)
    minDuration = Column(Integer)
    maxDuration = Column(Integer)
    sumDuration = Column(Integer)
    app_name = Column(String(50))
    test_env = Column(String(50))
    test_product = Column(String(50))
    test_project = Column(String(50))
    test_report = Column(String(255))

    def to_dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}


if __name__ == '__main__':
    from datetime import datetime
    import time
    import requests



    # get_summary('http://10.20.17.218:8080/job/AI_Jobs/view/AI-%E8%87%AA%E5%8A%A8%E5%8C%96%E6%B5%8B%E8%AF%95/job/AI-dsu-auto-test-all/allure/widgets/summary.json')
    # ci = AiReport(failed=20, broken=1, skipped=2, passed=54, unknown=0, total=75,
    #               start=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(1640137982670/1000)),
    #               stop=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(1640141698462/1000)),
    #               duration=3715792,
    #               minDuration=0,
    #               maxDuration=416183,
    #               sumDuration=2957834)
    # print(ci)
    #
    # print(ci.__tablename__)
    # SaveDB().save_to_db(ci.__tablename__, ci)
