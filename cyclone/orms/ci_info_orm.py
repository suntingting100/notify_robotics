#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:yang wei
@file:ci_info_orm.py
@time:2021/10/27
"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

from cyclone.utils.save_db import SaveDB

Base = declarative_base()


class CiInfo(Base):
    __tablename__ = 'ci_info'

    id = Column(Integer, primary_key=True)
    project = Column(String(50))
    build_Number = Column(Integer)
    tag = Column(String(50))
    branch = Column(String(50))
    ci_status = Column(String(50))
    cd_status = Column(String(50))

    def to_dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}


if __name__ == '__main__':
    Base.metadata.create_all(SaveDB().engine)
    ci = CiInfo(project='test', build_Number=111, tag='test-a-a', branch='master', ci_status='success')
    print(ci)
    SaveDB().save_to_db(ci.__tablename__, ci)
