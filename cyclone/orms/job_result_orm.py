#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:yang wei
@file:ci_info_orm.py
@time:2021/10/27
"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, Float

from cyclone.utils.save_db import SaveDB

Base = declarative_base()


class JobResult(Base):
    __tablename__ = 'job_result'

    id = Column(Integer, primary_key=True)
    line = Column(String(50))
    user = Column(String(50))
    job_name = Column(String(50))
    build_number = Column(Integer)
    env = Column(String(50))
    ci = Column(String(50))
    cd = Column(String(50))
    test = Column(String(50))
    duration_time = Column(Float)
    branch = Column(String(50))
    status = Column(String(50))

    def to_dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}


if __name__ == '__main__':
    ci = JobResult(line='AI', user='test', job_name='ai-test', build_number=111, env='test', branch='master', ci=str(True), cd=False, test=False, duration_time=10.11, status='success')
    print(ci)
    SaveDB().save_to_db(ci.__tablename__, ci)
