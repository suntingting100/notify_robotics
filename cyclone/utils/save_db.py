#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:yang wei
@file:save_db.py
@time:2021/11/05
"""
import urllib

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from cyclone import setting


class SaveDB:
    def __init__(self):
        password = urllib.parse.quote_plus(setting.db_passwd)
        engine = create_engine('mysql+pymysql://%s:%s@%s:%s/%s' % (
            setting.db_user, password, setting.db_host,
            setting.db_port, setting.db_name))
        # engine = create_engine("mysql+pymysql://data_writer:cyclone_qa@10.20.17.176:30086/qcenter")
        self.conn = engine.connect()
        self.engine = engine

    def save_to_db(self, table_name, df_to_be_written):
        table_to_write_to = table_name

        listToWrite = df_to_be_written.to_dict()
        metadata = sqlalchemy.schema.MetaData(bind=self.engine)
        table = sqlalchemy.Table(table_to_write_to, metadata, autoload=True)
        Session = sessionmaker(bind=self.engine)
        session = Session()
        session.execute(table.insert().prefix_with("IGNORE"), listToWrite)
        session.commit()
        session.close()


if __name__ == '__main__':
    config = setting
    print(config.db_passwd)
    pass
