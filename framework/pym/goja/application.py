# coding=utf-8
# -*- coding: utf-8 -*-
#
# Copyright 2014 by sogyf. All Rights Reserved.
import os
import sys

from goja.utils import underline_to_camel, storage_file, upper_first
from goja.utils import copy_directory, read_conf
from jinja2 import Environment, FileSystemLoader

__author__ = 'sogyf'


class Application:
    """
        Goja Framework Application
    """

    def __init__(self, cmd_path, goja_home, application_name):
        """
        初始化对象
        :param cmd_path: 当前执行命令的地址
        :param goja_home: Goja_Home 的地址
        :param application_name: 应用名称
        """
        self.cmd_path = cmd_path
        self.goja_home = goja_home

        self.application_name = application_name
        if not cmd_path.endswith(application_name):
            self.app_dir = os.path.join(self.cmd_path, self.application_name)
        else:
            self.app_dir = self.cmd_path
            # if not os.path.exists(self.app_dir):
            #     print '应用目录 ' + self.app_dir + ' 不存在,无法执行命令'
            #     sys.exit(1)

    def layout(self):
        self.mk_java_dir()
        self.mk_misc_dir()

    def sync_lib(self):
        storage_path = os.path.join(self.app_dir, 'src', 'main', 'webapp', 'WEB-INF', 'lib')
        copy_directory(os.path.join(self.goja_home, 'resources', 'libs'), storage_path)

        storage_path = os.path.join(self.app_dir, 'src', 'test', 'lib')
        copy_directory(os.path.join(self.goja_home, 'resources', 'libs-test'), storage_path)

    def conf(self):
        storage_path = os.path.join(self.app_dir, 'src', 'main', 'resources')
        params = {'appName': self.application_name}

        file_content = self.__code_tpl__('conf/application.conf', params)
        storage_file(storage_path, file_content, 'application.conf')

    def code(self):
        # .gitignore copy
        ignore_git = open(os.path.join(self.goja_home, 'resources', 'git', 'ignore'), 'r')
        storage_file(self.app_dir, ignore_git.read(), '.gitignore')
        ignore_git.close()

        storage_path = os.path.join(self.app_dir, "src", "main", "java", "app", "controllers")

        params = {'appName': self.application_name}

        file_content = self.__code_tpl__('code/IndexController.jinja2', params)
        storage_file(storage_path, file_content, 'IndexController.java')

        storage_path = os.path.join(self.app_dir, "src", "main", "webapp", "WEB-INF", "views")

        file_content = self.__code_tpl__('code/index.jinja2', params)
        storage_file(storage_path, file_content, 'index.ftl')

    def pom(self):
        params = {'group': self.application_name}

        file_content = self.__code_tpl__('maven/pomTemplate.xml', params)
        storage_file(self.app_dir, file_content, 'pom.xml')

        prod_xml = open(os.path.join(self.goja_home, 'resources', 'protable', 'prod.xml'), 'r')
        storage_file(os.path.join(self.app_dir, "misc", "portable"), prod_xml.read(), 'prod.xml')
        prod_xml.close()
        print('generate maven pom file Success!')

    def pack_war(self):
        import subprocess

        # 1. render build.xml file into project dir.
        war_params = {'appName': self.application_name,
                      'genPath': self.goja_home}
        build_xml_content = self.__code_tpl__('build/build.xml', war_params)
        build_xml_file = os.path.join(self.app_dir, 'build.xml')
        storage_file(self.app_dir, build_xml_content, 'build.xml')

        # 2. call ant run subprocess.
        ant_path = os.path.join(self.goja_home, 'resources', 'ant', 'bin', 'ant')
        ant_cmds = '%s clean package' % ant_path
        compile_process = subprocess.Popen(ant_cmds, shell=True, stdout=subprocess.PIPE)
        while compile_process.poll() is None:
            print(compile_process.stdout.readline())
        # 3. clean build file.
        os.remove(build_xml_file)

    def __appname__(self):
        """
            读取项目名称
        :return: 读取项目名称
        """
        conf = read_conf(self.app_dir)
        return conf['app.name']

    def syncdb(self):
        """
            sync database with model. only mysql.

        """
        conf = read_conf(self.app_dir)
        if 'db.url' not in conf:
            print('The Application not enable database or not mysql database.')
            sys.exit()
        # 读取生成规则
        generate_model = 'app.models'
        if 'generate.model' in conf:
            generate_model = conf['generate.model']
        generate_base_model = generate_model + '.base'
        if 'generate.model.base' in conf:
            generate_base_model = conf['generate.model.base']

        model_path = generate_model.split('.')
        base_model_path = generate_base_model.split('.')

        # 解析数据库配置
        db_url = conf['db.url']
        host_index = db_url.find(':', 12)
        host = db_url[13:host_index]
        port_idx = db_url.find('/', host_index)
        # port = db_url[host_index + 1: port_idx]
        db_name = db_url[port_idx + 1: db_url.find('?', port_idx)]

        db_user = conf['db.username']
        db_pwd = conf['db.password']

        # 读取数据库信息
        import MySQLdb
        import getpass

        db = MySQLdb.connect(host, db_user, db_pwd, db_name)
        cursor = db.cursor()
        sql = 'show tables'

        models = []

        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            for row in results:
                # table name like ol_member_type
                real_table_name = row[0]
                row__find = real_table_name.find('_')
                _rtn = real_table_name[row__find + 1: len(real_table_name)]
                table_name = 'tmp_%s' % _rtn
                # find table column name
                cursor.execute(
                    "select column_name,data_type from information_schema.columns where table_name='%s'" % real_table_name)
                columns = cursor.fetchall()
                column_list = []
                column_models = []
                for column in columns:
                    column_list.append(column[0])
                    field_var = underline_to_camel(column[0])
                    column_models.append({
                        'name': column[0],
                        'fieldName': upper_first(field_var),
                        'fieldvar': field_var,
                        'data_type': column[1]
                    })
                model_file = underline_to_camel(table_name).replace('tmp', '')
                models.append({
                    'model': model_file,
                    'table': real_table_name,
                    'columns': ','.join(column_list),
                    'column_models': column_models
                })

            cursor.close()
        except:
            import traceback
            traceback.print_exc()
            print("error unkown tables;")
        finally:
            db.close()

        src_java_dir = os.path.join(self.app_dir, 'src', 'main', 'java')
        model_dir = os.path.join(src_java_dir, *model_path)
        base_model_dir = os.path.join(src_java_dir, *base_model_path)
        # 打印目录
        print('generate db model in [%s]' % base_model_dir)
        print('generate db base model in [%s]' % model_dir)
        scd = os.path.join(self.app_dir, 'src', 'main', 'resources', 'sqlconf')
        sys_user = getpass.getuser()

        for _m in models:
            _tm = _m['model']
            _lm = _tm.lower()

            _table_name = _m['table']
            params = {
                'tableName': _table_name,
                'model': _tm,
                'lower_model': _lm,
                'sysUser': sys_user,
                'pkg': generate_base_model
            }
            file_content = self.__code_tpl__('code/model.jinja2', params)
            if not os.path.exists(os.path.join(model_dir, _tm + '.java')):
                storage_file(model_dir, file_content, _tm + ".java")

            base_model_params = {
                'tableName': _table_name,
                'model': _tm,
                'sysUser': sys_user,
                'columns': _m['column_models'],
                'pkg': generate_base_model
            }
            base_model_content = self.__code_tpl__('code/basemodel.jinja2', base_model_params)
            if not os.path.exists(os.path.join(base_model_dir, 'Base' + _tm + '.java')):
                storage_file(base_model_dir, base_model_content, "Base" + _tm + ".java")

            sql_params = {'model': _lm, 'columns': _m['columns'], 'tableName': _table_name}
            sql_conf_content = self.__code_tpl__('code/sql.jinja2', sql_params)
            if not os.path.exists(os.path.join(scd, _lm + '-sql.xml')):
                storage_file(scd, sql_conf_content, _lm + '-sql.xml')
        print('sync db to model Success!')

    def idea(self):
        """
        生成IDEA的工程
        :rtype : object
        """
        idea_ipr = self.application_name + '.ipr'
        idea_iml = self.application_name + '.iml'
        params = {
            'appName': self.application_name,
            'goja_home': self.goja_home
        }
        file_content = self.__code_tpl__('idea/imlTemplate.xml', params)
        storage_file(self.app_dir, file_content, idea_iml)
        file_content = self.__code_tpl__('idea/iprTemplate.xml', params)
        storage_file(self.app_dir, file_content, idea_ipr)
        print('Convert the Intellij idea project Success.')

    def __code_tpl__(self, tpl_file, params):
        env = Environment(
            # loader是加载器类，用来加载模板文件。
            loader=FileSystemLoader(os.path.join(self.goja_home, 'framework', 'templates')),
            auto_reload=True,  # 自动重载，调试用
            # 还有许多参数，例如缓存大小，详细见jinja2文档
        )
        # 创建一个template对象。
        template = env.get_template(tpl_file)
        # 进行渲染，返回HTML字符串。
        return template.render(params)

    def mk_java_dir(self):
        """
            创建工程目录
            ── misc
            │   ├── docs
            │   ├── portable
            │   └── scripts
            └── src
            ├── main
            │   ├── java
            │   │   └── app
            │   ├── resources
            │   │   ├── application.conf
            │   │   └── sqlconf
            │   └── webapp
            │       ├── WEB-INF
            │       └── static
            └── test
                └── java

        """
        _src = os.path.join(self.cmd_path, self.application_name, 'src')
        if os.path.exists(_src):
            print('the %s is exist!' % os.path.join(self.cmd_path, self.application_name))
            sys.exit(1)
        os.makedirs(_src)
        main_ = os.path.join(_src, 'main')
        os.mkdir(main_)
        java_ = os.path.join(main_, 'java')
        os.mkdir(java_)
        app_path = os.path.join(java_, 'app')
        os.mkdir(app_path)
        os.mkdir(os.path.join(app_path, 'controllers'))
        os.mkdir(os.path.join(app_path, 'models'))
        os.mkdir(os.path.join(app_path, 'models', 'base'))
        os.mkdir(os.path.join(app_path, 'jobs'))
        os.mkdir(os.path.join(app_path, 'interceptors'))
        os.mkdir(os.path.join(app_path, 'validators'))
        os.mkdir(os.path.join(app_path, 'dtos'))

        resources_ = os.path.join(main_, 'resources')
        os.mkdir(resources_)
        os.mkdir(os.path.join(resources_, 'sqlconf'))

        webapp_ = os.path.join(main_, 'webapp')
        os.mkdir(webapp_)
        os.mkdir(os.path.join(webapp_, 'static'))
        web_inf_ = os.path.join(webapp_, 'WEB-INF')
        os.mkdir(web_inf_)
        os.mkdir(os.path.join(web_inf_, 'views'))

        test_ = os.path.join(_src, 'test')
        os.mkdir(test_)
        test_java_ = os.path.join(test_, 'java')
        os.mkdir(test_java_)
        os.mkdir(os.path.join(test_java_, 'app'))
        os.mkdir(os.path.join(test_, 'resources'))

    def mk_misc_dir(self):
        misc = os.path.join(self.cmd_path, self.application_name, 'misc')
        os.makedirs(misc)
        os.mkdir(os.path.join(misc, "docs"))
        os.mkdir(os.path.join(misc, "portable"))
        os.mkdir(os.path.join(misc, "scripts"))
