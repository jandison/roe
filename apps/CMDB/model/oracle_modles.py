# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from CMDB.model.yewutree_model import YewuTree
from django.contrib.auth.models import User




#群，一定属于某一个产品线，可能属于多个组,一个节点也是群
class OracleCluster(models.Model):
    arch = (
        (u"主从", u"主从"),
        (u"单机", u"单击"),
        (u"rac", u"rac"),
        (u"rac+从库", u"rac+从库")
    )
    name = models.CharField(u"集群名", max_length=30, blank=True,null=True)
    arch = models.CharField(verbose_name=u"集群架构", choices=arch, max_length=30, null=True, blank=True)
    db_version = models.CharField(verbose_name=u"数据库版本",  max_length=30, null=True, blank=True)
    defaultdb=models.CharField(verbose_name=u"主用DB",  max_length=30, null=True, blank=True)
    tree_id=models.ForeignKey(YewuTree,verbose_name=u"所属产品线", on_delete=models.SET_NULL, null=True, blank=True)
    desc = models.CharField(u"描述", max_length=100, null=True, blank=True)
    operator = models.ManyToManyField(User, verbose_name="可见的人", blank=True)
    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'Oracle_Cluster'
        verbose_name = 'Oracle 集群'
        verbose_name_plural = 'Oracle集群'



# 按照用户来划分产品线
class OracleUser(models.Model):
    db_user = models.CharField(max_length=30, null=True,blank=True)
    db_password=models.CharField(max_length=60, null=True,blank=True)
    privlige=models.CharField(verbose_name='权限',max_length=400, null=True,blank=True)
    dbcluster = models.ForeignKey(OracleCluster,verbose_name=u"所属集群", on_delete=models.SET_NULL, null=True, blank=True)

    def __unicode__(self):
        return self.db_user
    class Meta:
        db_table = 'Oracle_User'
        verbose_name = 'Oracle用户'
        verbose_name_plural = 'Oracle用户'

#数据库中的 DB，表空间信息
class Oracletablespace(models.Model):
        tablespace_name = models.CharField(max_length=50,verbose_name=u"表空间名")
        dbcluster = models.ForeignKey(OracleCluster,verbose_name=u"所属集群", on_delete=models.SET_NULL, null=True, blank=True)
        tablespace_size=models.CharField(max_length=50,verbose_name=u"库大小")
        def __unicode__(self):
            return u'%s ' % ( self.tablespace_name)

        class Meta:
            db_table = 'Oracle_Tablespace'
            verbose_name = 'Oracle 表空间'
            verbose_name_plural = 'Oracle表空间'



#ORACLE 实例表。配置信息慢慢添加
class Oracle_Instance(models.Model):
    DB_ROLE = (
        (u"单库", u"单库"),
        (u"主库", u"主库"),
        (u"从库", u"从库"),
        (u"汇总", u"汇总")
    )

    DB_STATUS = (
        (u"使用中", u"使用中"),
        (u"未使用", u"未使用"),
        (u"故障", u"故障"),
        (u"其它", u"其它"),
    )
    dbtag = models.CharField(max_length=50, verbose_name=u"数据库标志", blank=True,null=True)
    vist_ip = models.GenericIPAddressField(verbose_name=u"访问VIP", max_length=15)
    m_ip =  models.GenericIPAddressField(verbose_name=u"管理IP", max_length=15)
    other_ip= models.CharField(max_length=150, verbose_name=u"其他IP,逗号隔开")
    port = models.IntegerField(verbose_name=u"端口",default=1521)
    sid = models.CharField(verbose_name=u"SID", max_length=8,blank=True,null=True)
    idc = models.CharField(verbose_name=u"机房", max_length=18,blank=True,null=True)
    CLUSTER = models.ForeignKey(OracleCluster, verbose_name=u"所属集群", on_delete=models.SET_NULL, null=True, blank=True)
    role = models.CharField(verbose_name=u"DB角色", choices=DB_ROLE, max_length=30, null=True, blank=True)
    db_status = models.CharField(verbose_name=u"DB状态", choices=DB_STATUS, max_length=30, null=True, blank=True)
    memory = models.CharField(u"分配内存", max_length=30, null=True, blank=True)
    disk = models.CharField(u"磁盘位置", max_length=200, null=True, blank=True)
    memo = models.TextField(u"备注信息", max_length=200, null=True, blank=True)
    def __unicode__(self):
        return self.dbtag
    class Meta:
        db_table = 'Oracle_Instance'
        verbose_name = 'Oracle集群一个实例'
        verbose_name_plural = 'Oracle集群一个实例'