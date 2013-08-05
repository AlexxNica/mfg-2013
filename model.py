import web, datetime,mfg
from xml.dom import minidom
import codecs
import os.path, time

# db = web.database(dbn='mysql', db='blog', user='root', pw='' )
db = web.database(dbn='mysql', db='blog', user='wei', pw='' )

   
def xxmlat(s, dbob, sattr, val, iro):

   if str(dbob) != 'None' :
      if not s.hasAttribute(sattr) :
          s.setAttribute(sattr,"")

      if val == '' :
          s.attributes[sattr] = str(dbob)
      else : 
          if iro > 0 :
            s.attributes[sattr] = round(val,iro)
         
   else :
      if s.hasAttribute(sattr) :
          s.removeAttribute(sattr)

def xxmrlat( inum, s, sattr ):
             
   if s.hasAttribute(sattr) :
       val = s.getAttribute(sattr)
       update_glyphparamD( inum, sattr, val)

def delFont(fontName,glyphNamel):

  return None

def putFont():
#
#  put font A and font B into table
#
  idworks = mfg.cFont.idwork
  mfg.cFont.fontpath="fonts/"+str(mfg.cFont.idmaster)+"/"
  
  print mfg.cFont.glyphName
  print mfg.cFont.glyphunic
  global glyphsource
  global glyphnameNew
  global glyphName
  glyphName = mfg.cFont.glyphunic 
  glyphsourceA = mfg.cFont.fontpath+mfg.cFont.fontna + "/glyphs/"+glyphName+".glif"
  glyphsourceB = mfg.cFont.fontpath+mfg.cFont.fontnb + "/glyphs/"+glyphName+".glif"
  glyphnameNew = glyphName+".glif"
  print glyphnameNew
  print "lastmodifiedA: %s" % time.ctime(os.path.getmtime(glyphsourceA))
  print "lastmodifiedB: %s" % time.ctime(os.path.getmtime(glyphsourceB))

  global xmldocA
  global xmldocB
  global itemlistA
  global itemlistB
  try :
     xmldocA = minidom.parse(glyphsourceA)
     xmldocB = minidom.parse(glyphsourceB)
  except :
     print "not meier"
     return None

  advanceA = xmldocA.getElementsByTagName('advance')
  advanceB = xmldocB.getElementsByTagName('advance')
  
  idmasterA = int(mfg.cFont.idmaster)
  idmasterB = -idmasterA

  idsA= " and idmaster="+'"'+str(idmasterA)+'"'
  idsB= " and idmaster="+'"'+str(idmasterB)+'"'
#
#  decide when to load new entries from xml file   
#
  dbqA= list(db.query("SELECT unix_timestamp(max(vdate)) vdate from glyphoutline where glyphname=glyphName" +idsA))
  dbqB= list(db.query("SELECT unix_timestamp(max(vdate)) vdate from glyphoutline where glyphname=glyphName" +idsB))
  dbqpA= list(db.query("SELECT unix_timestamp(max(vdate)) vdate from glyphparam where glyphname=glyphName"+idsA))
  dbqpB= list(db.query("SELECT unix_timestamp(max(vdate)) vdate from glyphparam where glyphname=glyphName"+idsB))
# check if glyphoutline exists
  for idmaster in [idmasterA, idmasterB] :
    if idmaster == idmasterA:
      mfg.cFont.idwork='0'
      glyphsource = glyphsourceA
      dbq = dbqA
      if  dbqA[0].vdate == None :
         vdatedb = 0
         vdatedbp = 0
      else:
         vdatedb=int(dbqA[0].vdate)
         if dbqpA[0].vdate == None :
            vdatedbp = 0
         else:
            vdatedbp=int(dbqpA[0].vdate)
      ids = idsA
      itemlist = xmldocA.getElementsByTagName('point')

    if idmaster == idmasterB:
      mfg.cFont.idwork='1'
      glyphsource = glyphsourceB
      dbq = dbqB
      if  dbqB[0].vdate == None :
         vdatedb = 0
         vdatedbp = 0
      else:
         vdatedb=int(dbqB[0].vdate)
         if dbqpB[0].vdate == None :
            vdatedbp = 0
         else:
            vdatedbp=int(dbqpB[0].vdate)
      ids = idsB
      itemlist = xmldocB.getElementsByTagName('point')

    if dbq:
      vdateos=int(os.path.getmtime(glyphsource))
      idel =0 
      if ( max(vdatedb,vdatedbp) < vdateos) and mfg.cFont.loadoption =='0' or mfg.cFont.loadoption =='99'  :
        db.delete('glyphoutline', where='Glyphname="'+glyphName+'"'+ids )  
        db.delete('glyphparam', where='Glyphname="'+glyphName+'"'+ids )  
        idel=1

# check if list is empty
    if not  list(db.select('glyphoutline', where='GlyphName="'+glyphName+'"'+ids )) or mfg.cFont.loadoption == '1' : 
#  put data into db
      inum=0
      strg=""
      for s in itemlist :
        inum = inum+1
#  find a named point , convention the name begin with the letter z
        if mfg.cFont.loadoption == '0' or idel ==1:
          if s.hasAttribute('name'): 
            im = s.attributes['name'] 
            iposa = im.value.find("z")
            ipose = im.value.find(",",iposa)
            if ipose > iposa :
               nameval = im.value[iposa:ipose]
            else :
               if ipose == -1 :
                 ipose=len(im.value) 
                 nameval = im.value[iposa:ipose]
            idpar=inum
            db.insert('glyphparam', id=inum,GlyphName=glyphName, idmaster=idmaster, PointName=nameval)

#  find  all parameter and save it in db
# add glyphparameters here:
            xxmrlat( inum, s, 'groupname')
            xxmrlat( inum, s, 'startp' )
            xxmrlat( inum, s, 'doubledash' )
            xxmrlat( inum, s, 'tripledash')
            xxmrlat( inum, s, 'superleft')
            xxmrlat( inum, s, 'superright')
            xxmrlat( inum, s, 'leftp')
            xxmrlat( inum, s, 'rightp')
            xxmrlat( inum, s, 'downp')
            xxmrlat( inum, s, 'upp')
            xxmrlat( inum, s, 'dir')
            xxmrlat( inum, s, 'tension')
            xxmrlat( inum, s, 'tensionand')
            xxmrlat( inum, s, 'cycle')
            xxmrlat( inum, s, 'penshifted')
            xxmrlat( inum, s, 'pointshifted')
            xxmrlat( inum, s, 'angle')
            xxmrlat( inum, s, 'penwidth')
            xxmrlat( inum, s, 'overx')
            xxmrlat( inum, s, 'overbase')
            xxmrlat( inum, s, 'overcap')
            xxmrlat( inum, s, 'overasc')
            xxmrlat( inum, s, 'overdesc')
            xxmrlat( inum, s, 'ascpoint')
            xxmrlat( inum, s, 'descpoint')
            xxmrlat( inum, s, 'stemcutter')
            xxmrlat( inum, s, 'stemshift')
            xxmrlat( inum, s, 'inktrap_l')
            xxmrlat( inum, s, 'inktrap_r')

          else :
            nameval = ""
            startp = 0
            idpar =  None

          s.attributes['pointNo']= "p" + str(inum)    # adding a new attribute

          if s.hasAttribute('type') : 
              mainpoint = 1
          else :
             mainpoint = 0 
          if idpar == None :
              strg= "insert into glyphoutline (GlyphName,PointNr,x,y,contrp,id,idmaster,pip) Values ("+'"'+glyphName+'"'+","+'"'+s.attributes['pointNo'].value+'"' + ","+ str(s.attributes['x'].value)+ "," + str(s.attributes['y'].value)+","+str(mainpoint)+","+str(inum)+","+str(idmaster)+",NULL)"
          else:
              strg= "insert into glyphoutline (GlyphName,PointNr,x,y,contrp,id,idmaster,pip) Values ("+'"'+glyphName+'"'+","+'"'+s.attributes['pointNo'].value+'"' + ","+ str(s.attributes['x'].value)+ "," + str(s.attributes['y'].value)+","+str(mainpoint)+","+str(inum)+","+str(idmaster)+","+str(idpar)+")"
          db.query(strg)
          db.query("commit") 
        if mfg.cFont.loadoption == '1' and idel <1:
          if s.hasAttribute('type') : 
              mainpoint = 1
          else :
             mainpoint = 0 
          update_postp0(inum, s.attributes['x'].value, s.attributes['y'].value, str(mainpoint))
#    in this case we read only the coordinates from the xml file
          if s.hasAttribute('name'): 
            im = s.attributes['name'] 
            iposa = im.value.find("z")
            ipose = im.value.find(",",iposa)
            if ipose > iposa :
               nameval = im.value[iposa:ipose]
            else :
               if ipose == -1 :
                 ipose=len(im.value) 
                 nameval = im.value[iposa:ipose]
            pip=get_glyphparamid (glyphName, idmaster, nameval)
            update_postp(inum, s.attributes['x'].value, s.attributes['y'].value, pip)

#   save previous value back          
  mfg.cFont.idwork = idworks 
  return None  

def gidmast(idwork):
    if idwork == '0':
       idmaster = int(mfg.cFont.idmaster)
    if idwork == '1':
       idmaster = -int(mfg.cFont.idmaster)
    return(idmaster)

def get_posts():
    idmaster = gidmast(mfg.cFont.idwork)
    glyphName = mfg.cFont.glyphunic 
    ids= " and idmaster="+'"'+str(idmaster)+'"'
    q1="SELECT IFNULL(PointName, '') PointNr,x,y,concat('position:absolute;left:',0+x,'px;top:',0-y,'px; ',IF (PointName > '', 'color:black;', IF (contrp > 0 , 'z-index:-1;color:blue;', 'z-index:-2;color:CCFFFF;')) ) position, id from vglyphoutline where GlyphName="+'"'+glyphName+'"'
    return list(db.query(q1+ids ))

def get_postspa():
    idmaster = gidmast(mfg.cFont.idwork)
    glyphName = mfg.cFont.glyphunic 
    ids= " and idmaster="+'"'+str(idmaster)+'"'
#    dbstr=db.select('vglyphoutlines', where='glyphName='+'"'+glyphName+'"' +ids, vars=locals())     
    dbstr=db.select('vgls', where='glyphName='+'"'+glyphName+'"' +ids+' order by length(PointName) asc,PointName asc', vars=locals())     
    return list(dbstr)


def get_post(id):
    glyphName = mfg.cFont.glyphunic 
    idmaster = gidmast(mfg.cFont.idwork)
    ids= " and idmaster="+'"'+str(idmaster)+'"'
    try:
        return db.select('vglyphoutline', where='id=$id and glyphName='+'"'+glyphName+'"' +ids, vars=locals())[0]
    except IndexError:
        return None

def get_postspip():
    glyphName = mfg.cFont.glyphunic 
    idmaster = gidmast(mfg.cFont.idwork)
    ids= " and idmaster="+'"'+str(idmaster)+'"'
    q1="SELECT id,pip from glyphoutline where GlyphName="+'"'+glyphName+'"'
    return list(db.query(q1+ids))

def get_glyphparamid(glyphName, idmaster,nameval):

    ids= " and idmaster="+'"'+str(idmaster)+'"'
    strg="select id from glyphparam where GlyphName='"+glyphName+"' and PointName ='"+nameval+"'"+ids
    dbstr=list(db.query(strg))
    if dbstr == [] :
      return None
    else:
      return dbstr[0].id

def get_glyphparam(id):
    glyphName = mfg.cFont.glyphunic 
    idmaster = gidmast(mfg.cFont.idwork)
    ids= " and idmaster="+'"'+str(idmaster)+'"'
    try:
#        return db.select('glyphparam', where='id=$id and GlyphName='+'"'+glyphName+'"'+ids, vars=locals())[0]
        return db.select('vglyphoutlines', where='id=$id and GlyphName='+'"'+glyphName+'"'+ids, vars=locals())[0]
    except IndexError:
        return None

def get_groupparam(id):
    glyphName = mfg.cFont.glyphunic 
    idmaster = gidmast(mfg.cFont.idwork)
    ids= " and idmaster="+'"'+str(idmaster)+'"'
    try:
        return db.select('vglgroup', where='id=$id and GlyphName='+'"'+glyphName+'"'+ids, vars=locals())[0]
    except IndexError:
        return None

def get_groupparam0(groupname):
    idmaster = gidmast(mfg.cFont.idwork)
    ids= " and idmaster="+'"'+str(idmaster)+'"'
    try:
       return db.select('groupparam', where='groupname='+'"'+groupname+'"'+ids, vars=locals())[0]
    except IndexError:
       return None


def update_post(id, x, y):
    glyphName = mfg.cFont.glyphunic 
    idmaster = gidmast(mfg.cFont.idwork)
    ids= " and idmaster="+'"'+str(idmaster)+'"'
    
    db.update('glyphoutline', where='id=$id and GlyphName="'+glyphName+'"'+ids, vars=locals(),
        x=x, y=y)

    db.query("commit")
    return None

def update_postp0(id, x, y, contr):
    glyphName = mfg.cFont.glyphunic 
    idmaster = gidmast(mfg.cFont.idwork)
    ids= " and idmaster="+'"'+str(idmaster)+'"'
#  remove pip link and set coordinates and contr new     
    db.update('glyphoutline', where='id=$id and GlyphName="'+glyphName+'"'+ids, vars=locals(),
        x=x, y=y, pip=None, contrp=contr)
    db.query("commit")
    return None

def update_postp(id, x, y, idpar ):
    glyphName = mfg.cFont.glyphunic 
    idmaster = gidmast(mfg.cFont.idwork)
    ids= " and idmaster="+'"'+str(idmaster)+'"'
    
    if x == None :
           db.update('glyphoutline', where='id=$id and GlyphName="'+glyphName+'"'+ids, vars=locals(),
                     pip=idpar)
    else:
           db.update('glyphoutline', where='id=$id and GlyphName="'+glyphName+'"'+ids, vars=locals(),
        x=x, y=y, pip=idpar)

    db.query("commit")
    return None

def update_glyphparamD(id, ap, bp):
# string:syntax update glyphparam set leftp='1' where id=75 and Glyphname='p' and idmaster=1;
    glyphName = mfg.cFont.glyphunic 
    idmaster = gidmast(mfg.cFont.idwork)
    ids= " and idmaster="+'"'+str(idmaster)+'"'
#
#   get id from glyphoutline
    strg="select pip from glyphoutline where id='"+str(id)+"' and glyphname='"+glyphName+"'"+ids
    lli=list(db.query(strg))
    strg =""
    if lli == [] :
        idp=id
        update_postp(id, None, None, idp)
    else:         
        idp=str(lli[0].pip)
    print "link id,pip",id,idp

#
    if ap in ['','select'] :
      return None
    aa = ap 
    if bp != '' :
      bb = bp 
      bbstr=str(bb) 
      strg="update glyphparam set "+aa+"="+"'"+bbstr+"'"+" where id="+str(idp)+" and GlyphName='"+glyphName+"'"+ids 
    else:
      strg="update glyphparam set "+aa+"=NULL where id="+str(idp)+" and GlyphName='"+glyphName+"'"+ids 
    print strg
    db.query(strg)
    db.query("commit")
    return None
  
def update_glyphparam(id, a, b):
    glyphName = mfg.cFont.glyphunic 
    idmaster = gidmast(mfg.cFont.idwork)
    ids= " and idmaster="+'"'+str(idmaster)+'"'
#
#   get id from glyphoutline
    strg="select pip from glyphoutline where id='"+str(id)+"' and glyphname='"+glyphName+"'"+ids
    lli=list(db.query(strg))
    idp=str(lli[0].pip)
    print "link id,pip",id,idp
#
    if a != '' :
      aa = a
    else:
      db.update('glyphparam', where='id="'+idp+'" and GlyphName="'+glyphName+'"'+ids, vars=locals(),
        pointName=None, groupname=None)
      db.query("commit")
      return None 
    if b != '' :
      bb = b
      db.update('glyphparam', where='id="'+idp+'" and GlyphName="'+glyphName+'"'+ids, vars=locals(),
        pointName=aa, groupname=bb)
      db.query("commit")
      return None 
    else:
      db.update('glyphparam', where='id="'+idp+'" and GlyphName="'+glyphName+'"'+ids, vars=locals(),
        pointName=aa, groupname=None)
      db.query("commit")
      return None 

def update_glyphparamName(id, a):
    glyphName = mfg.cFont.glyphunic 
    idmaster = gidmast(mfg.cFont.idwork)
    ids= " and idmaster="+'"'+str(idmaster)+'"'
#
#   get id from glyphoutline
    strg="select pip from glyphoutline where id='"+str(id)+"' and glyphname='"+glyphName+"'"+ids
    lli=list(db.query(strg))
    idp=str(lli[0].pip)
    print "link id,pip",id,idp
#
    if a != '' :
      aa = a
      db.update('glyphparam', where='id="'+idp+'" and GlyphName="'+glyphName+'"'+ids, vars=locals(),
        pointName=aa)
      db.query("commit")
      return None
    else:
      db.update('glyphparam', where='id="'+idp+'" and GlyphName="'+glyphName+'"'+ids, vars=locals(),
        pointName=None)
      db.query("commit")
      return None

def update_glyphparamG(id, a):
    glyphName = mfg.cFont.glyphunic 
    idmaster = gidmast(mfg.cFont.idwork)
    ids= " and idmaster="+'"'+str(idmaster)+'"'
#
#   get id from glyphoutline
    strg="select pip from glyphoutline where id='"+str(id)+"' and glyphname='"+glyphName+"'"+ids
    lli=list(db.query(strg))
    idp=str(lli[0].pip)
#
    if a != '' :
      aa = a
      db.update('glyphparam', where='id="'+idp+'" and GlyphName="'+glyphName+'"'+ids, vars=locals(),
        pointName=aa)
      db.query("commit")
      return None
    else:
      db.update('glyphparam', where='id="'+idp+'" and GlyphName="'+glyphName+'"'+ids, vars=locals(),
        pointName=None)
      db.query("commit")
      return None

def insert_glyphparam(idp, a):
    
    glyphName = mfg.cFont.glyphunic 
    idmaster = gidmast(mfg.cFont.idwork)
    ids= " and idmaster="+'"'+str(idmaster)+'"'
    ligl=get_postspip()
    piplist=[]
    idlist=[]
    for liid in ligl :
      idlist.append (liid.id)
      if liid.pip not in [] :
         piplist.append (liid.pip)
    for idpa in idlist :  
      if idpa not in piplist : 
        print "insert glyphparam", idpa
        idpar=str(idpa) 
        break
    db.update('glyphoutline', where='id="'+str(idp)+'" and GlyphName="'+glyphName+'"'+ids, vars=locals(),
              pip=idpar)
    db.insert('glyphparam', id=idpar,GlyphName=glyphName, PointName=a, idmaster=idmaster)
    db.query("commit")
    return None

def update_groupparamD( groupname, a, b):
# string:syntax update groupparam set leftp='1' where id=75 and groupname='g1' and idmaster=1;
    print a,b
    glyphName = mfg.cFont.glyphunic 
    idmaster = gidmast(mfg.cFont.idwork)
    ids= " and idmaster="+'"'+str(idmaster)+'"'
    aa = a 
    print "*****group",groupname, a, b
    if a != None and a <> 'select' :
      if b != '' :
        bb = b 
        bbstr=str(bb) 
        strg="update groupparam set "+aa+"="+"'"+bbstr+"'"+" where groupname='"+groupname+"'"+ids 
      else:
        strg="update groupparam set "+aa+"=NULL where groupname='"+groupname+"'"+ids 
      print strg
      db.query(strg)
      db.query("commit")
    return None
  
def insert_groupparam( a):
    if a == ''  :
       return None 
    glyphName = mfg.cFont.glyphunic 
    idmaster = gidmast(mfg.cFont.idwork)
    db.insert('groupparam', groupname=a, idmaster=idmaster)
    db.query("commit")
    return None

def get_masters():
    return db.select('master',  vars=locals())

def get_master(id):

    mfg.cFont.idmaster=id
    ssmr= db.select('master',  where='idmaster=$id', vars=locals())
    ssm=list(ssmr)
    mfg.cFont.fontname=str(ssm[0].FontName)
    mfg.cFont.fontna=str(ssm[0].FontNameA)
    mfg.cFont.fontnb=str(ssm[0].FontNameB)
 
    return ssmr

def update_master(id):

    fontNameA=mfg.cFont.fontna
    fontNameB=mfg.cFont.fontnb
    fontName=mfg.cFont.fontname 
    db.update('master', where='idmaster=$id', vars=locals(),
       fontNameA=fontNameA,fontNameB=fontNameB,FontName=fontName)
    db.query("commit")
    return None

def get_globalparams():
    return db.select('globalparam', vars=locals())


def put_master():

    fontName=mfg.cFont.fontname
    fontNameA=mfg.cFont.fontna
    fontNameB=mfg.cFont.fontnb
    idglobal =mfg.cFont.idglobal
    t=db.transaction()
    
    try:
       db.insert('master', FontName="'"+fontName+"'", FontNameA="'"+fontNameA+"'", FontNameB="'"+fontNameB+"'", idglobal="'"+idglobal+"'")
    except:
       t.rollback()
       raise
    else:
       t.commit()

    return None    

def get_globalparams():
    return db.select('globalparam', vars=locals())

def get_globalparam(id):
    mfg.cFont.idglobal=id

    return db.select('globalparam', where='idglobal=$id',vars=locals())

def get_localparams():
    return db.select('localparam', vars=locals())

def get_localparam(id):
    print "idididget local",id
    return db.select('localparam', where='idlocal=$id',vars=locals())

def put_globalparam(id):

    metapolation=mfg.cFont.metapolation
    unitwidth=mfg.cFont.unitwidth
    fontsize = mfg.cFont.fontsize
    mean = mfg.cFont.mean
    cap = mfg.cFont.cap
    ascl = mfg.cFont.ascl
    des = mfg.cFont.des
    box = mfg.cFont.box
    db.insert('globalparam', where='idglobal = $id',vars=locals(), 
        metapolation=metapolation, unitwidth=unitwidth, fontsize=fontsize, mean=mean, cap=cap, ascl=ascl, des=des, box=box)
    db.query("commit")
    return None

def updatemaster(id, a, b, c, d):
    db.update('master', where='idmaster = $id', vars=locals(), 
      FontName = a, FontNameA = b, FontNameB = c, idglobal = d)
    db.query("commit")
    return None

def update_globalparam(id, a, b, c, d, e, f, g):
    db.update('globalparam', where='idglobal = $id', vars=locals(), 
      metapolation = a, fontsize = b, mean=c, cap=d, ascl=e, des=f, box=g)
    db.query("commit")
    return None

def update_localparam(id, a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13):
    print "id local param update",id
    db.update('localparam', where='idlocal = $id', vars=locals(), 
      px = a1, width=a2, space=a3, xheight=a4, capital=a5, boxheight=a6, ascender=a7, descender=a8, inktrap=a9, stemcut=a10, skeleton=a11, superness=a12, over=a13)
    db.query("commit")
    return None


def copyproject ():


  idmaster=int(mfg.cFont.idmaster)
#
# copy unix font ufo files
# 
# mkdir -p fonts/3
# cp -rpu fonts/1/* fonts/3/
#
  strg="select max(idmaster) maxid from master"
  idma=list(db.query(strg))
  idmasternew=idma[0].maxid  + 1
  print "idmasternew", idmasternew
#
  strg = "mkdir -p fonts/"+str(idmasternew)
  print "mkdir **",strg
  os.system(strg)
  strg = "cp -rp fonts/"+str(idmaster)+"/* fonts/"+str(idmasternew)+"/"
#
  print "cp **",strg
  os.system(strg)
#
#
  for iloop in [1,-1]:
    idmnew = "'"+str(iloop*idmasternew)+"'"
    idm = "'"+str(iloop*idmaster)+"'"
    strg="insert into master (idmaster,FontName,FontNameA,FontNameB,idglobal,vdate) select "+idmnew+", FontName,FontNameA,FontNameB,idglobal,now() from master where idmaster="+idm
    print strg
    db.query(strg)

    strg="drop table if exists tmp"
    db.query(strg)
    strg="create temporary table tmp select * from glyphoutline where idmaster="+idm
    db.query(strg)
    strg="update tmp set idmaster="+idmnew+",vdate=now() where idmaster="+idm 
    db.query(strg)
    strg="insert into glyphoutline select * from tmp where idmaster="+idmnew
    db.query(strg)

    strg="drop table if exists tmp"
    db.query(strg)
    strg="create temporary table tmp select * from groupparam where idmaster="+idm
    db.query(strg)
    strg="update tmp set idmaster="+idmnew+",vdate=now() where idmaster="+idm 
    db.query(strg)
    strg="insert into groupparam select * from tmp where idmaster="+idmnew
    db.query(strg)

    strg="drop table if exists tmp"
    db.query(strg)
    strg="create temporary table tmp select * from glyphparam where idmaster="+idm
    db.query(strg)
    strg="update tmp set idmaster="+idmnew+",vdate=now() where idmaster="+idm 
    db.query(strg)
    strg="insert into glyphparam select * from tmp where idmaster="+idmnew
    db.query(strg)
  return None


def writexml():


     glyphName = mfg.cFont.glyphunic 
     idmaster = gidmast(mfg.cFont.idwork)
      
     if mfg.cFont.idwork == '0' :
        glyphsourceA  = mfg.cFont.fontpath+mfg.cFont.fontna + "/glyphs/"+glyphName+".glif"
        glyphsource = glyphsourceA
        xmldocA = minidom.parse(glyphsourceA)
        itemlist = xmldocA.getElementsByTagName('point')

     if mfg.cFont.idwork == '1' :
        glyphsourceB = mfg.cFont.fontpath+mfg.cFont.fontnb + "/glyphs/"+glyphName+".glif"
        glyphsource = glyphsourceB
        xmldocB = minidom.parse(glyphsourceB)
        itemlist = xmldocB.getElementsByTagName('point')

     ids= " and idmaster="+'"'+str(idmaster)+'"'
     inum = 0
#     db_rows=list(db.query("SELECT PointName,x,y from glyphoutline"))
#    we assume the number of rows from the db >= the number of the itemlist 
     for  s in itemlist:
             inum = inum + 1
             qstr = "SELECT PointNr,x,y,PointName from vglyphoutline where id="+str(inum) +" and Glyphname="+'"'+glyphName+'"'+ids
            
             db_rows=list(db.query(qstr))
             s.attributes['pointNo'] = str(db_rows[0].PointNr)
             s.attributes['x'] = str(db_rows[0].x)
             s.attributes['y'] = str(db_rows[0].y)
             sname = str(db_rows[0].PointName)
               
             if sname not in ['','NULL', "None"] : 
                   qstrp = "SELECT * from  vglyphoutlines where id="+str(inum) +" and Glyphname="+'"'+glyphName+'"'+ids
                   db_rowpar = list(db.query(qstrp))
                   nameattr = sname
                   if s.hasAttribute('name') :
                      s.attributes['name']=nameattr
                   else :
                      s.setAttribute('name',nameattr)
#
#     first read group parameters
#                 
                   if str(db_rowpar[0].groupn) not in ["None",'NULL',''] :
                     groupname=db_rowpar[0].groupn

#     save the groupname in an xml attribute
#
                     if s.hasAttribute('groupname') :
                        s.attributes['groupname']=groupname
                     else :
                        s.setAttribute('groupname',groupname)

#     get the parameter list included with group parameters (lower priority)
                     qstrp = "SELECT * from vgls where id="+str(inum) +" and Glyphname="+'"'+glyphName+'"'+ids
                     db_rowpar = list(db.query(qstrp))

#
#      read param value and write into xml
#      add glyphparameters here:

                   xxmlat(s,db_rowpar[0].startp,'startp','1',0)
                   xxmlat(s,db_rowpar[0].doubledash,'doubledash','1',0)
                   xxmlat(s,db_rowpar[0].tripledash,'tripledash','1',0)
                   xxmlat(s,db_rowpar[0].superleft,'superleft','',5)
                   xxmlat(s,db_rowpar[0].superright,'superright','',5)
                   xxmlat(s,db_rowpar[0].leftp,'leftp','1',0)
                   xxmlat(s,db_rowpar[0].rightp,'rightp','1',0)
                   xxmlat(s,db_rowpar[0].downp,'downp','1',0)
                   xxmlat(s,db_rowpar[0].upp,'upp','1',0)
                   xxmlat(s,db_rowpar[0].dir,'dir','',0)
                   xxmlat(s,db_rowpar[0].leftp2,'leftp2','1',0)
                   xxmlat(s,db_rowpar[0].rightp2,'rightp2','1',0)
                   xxmlat(s,db_rowpar[0].downp2,'downp2','1',0)
                   xxmlat(s,db_rowpar[0].upp2,'upp2','1',0)
                   xxmlat(s,db_rowpar[0].dir2,'dir2','',0)
                   xxmlat(s,db_rowpar[0].tension,'tension','',0)
                   xxmlat(s,db_rowpar[0].tensionand,'tensionand','',0)
                   xxmlat(s,db_rowpar[0].cycle,'cycle','',0)
                   xxmlat(s,db_rowpar[0].penshifted,'penshifted','',0)
                   xxmlat(s,db_rowpar[0].pointshifted,'pointshifted','',0)
                   xxmlat(s,db_rowpar[0].angle,'angle','',0)
                   xxmlat(s,db_rowpar[0].penwidth,'penwidth','',0)
                   xxmlat(s,db_rowpar[0].overx,'overx','',0)
                   xxmlat(s,db_rowpar[0].overbase,'overbase','',0)
                   xxmlat(s,db_rowpar[0].overcap,'overcap','',0)
                   xxmlat(s,db_rowpar[0].overasc,'overasc','',0)
                   xxmlat(s,db_rowpar[0].ascpoint,'ascpoint','1',0)
                   xxmlat(s,db_rowpar[0].descpoint,'descpoint','1',0)
                   xxmlat(s,db_rowpar[0].stemcutter,'stemcutter','',4)
                   xxmlat(s,db_rowpar[0].stemshift,'stemshift','',4)
                   xxmlat(s,db_rowpar[0].inktrap_l,'inktrap_l','',4)
                   xxmlat(s,db_rowpar[0].inktrap_r,'inktrap_r','',4)
             else :
                   if s.hasAttribute('name') :
                      s.removeAttribute('name')
#
			
             s.toxml()
     print "glyphsource", glyphsource
     if mfg.cFont.idwork == '0' :
        with codecs.open(glyphsource, "w", "utf-8") as out:
          xmldocA.writexml(out) 
     if mfg.cFont.idwork == '1' :
        with codecs.open(glyphsource, "w", "utf-8") as out:
          xmldocB.writexml(out) 
     return None

def get_activeglyph():
    glyphName = mfg.cFont.glyphunic 
    idmaster = gidmast(mfg.cFont.idwork)
    ids= " idmaster="+'"'+str(idmaster)+'"'
    strg='select distinct(glyphname)  from glyphoutline where '+ids
    print strg
    return db.query(strg)


def writeallxmlfromdb():
     print "**** in writeallxmlfromdb "
     idworks=mfg.cFont.idwork
     for idwork in ['0','1']:
        mfg.cFont.idwork = idwork
        idmaster = mfg.cFont.idmaster
        idmaster = gidmast(mfg.cFont.idwork)
        ids= " idmaster="+'"'+str(idmaster)+'"'
        alist=list(get_activeglyph())
        for glyphn in alist :
          mfg.cFont.glyphunic = glyphn.glyphname
          mfg.cFont.glyphName = glyphn.glyphname
          writexml()
     mfg.cFont.idwork = idworks
     mfg.cFont.loadoption = '0'
     return None

def writeGlyphlist():
  ifile=open(mfg.cFont.fontpath+"glyphlist.mf","w")
  


  return None

def writeGlobalParam():
#
# prepare font.mf parameter file
# write the file into the directory mfg.cFont.fontpath
#  
  master = list(get_master(mfg.cFont.idmaster)) 
  imgl = list(get_globalparam(mfg.cFont.idglobal))

  mean=5.0
  cap=0.8
  ascl=0.2
  des=0.2
  box=1.0

  metapolation = imgl[0].metapolation
  u = imgl[0].unitwidth
  fontsize   = imgl[0].fontsize
  mean   = imgl[0].mean
  cap   = imgl[0].cap
  ascl   = imgl[0].ascl
  des   = imgl[0].des
  box   = imgl[0].box

# global parameters
  ifile=open(mfg.cFont.fontpath+"font.mf","w")
  ifile.write("% parameter file \n")
  ifile.write("metapolation:=%.2f;\n"%metapolation)
  ifile.write("font_size:=%.3fpt#;\n"%fontsize)
  ifile.write("mean#:=%.3fpt#;\n"%mean)
  ifile.write("cap#:=%.3fpt#;\n"%cap)
  ifile.write("asc#:=%.3fpt#;\n"%ascl)
  ifile.write("desc#:=%.3fpt#;\n"%des)
  ifile.write("box#:=%.3fpt#;\n"%box)
  ifile.write("u#:=%.3fpt#;\n"%u)

# local parameters A  
  imlo = list(get_localparam(mfg.cFont.idlocalA))

  ifile.write("A_px#:=%.2fpt#;\n"%imlo[0].px)
  ifile.write("A_width:=%.2f;\n"%imlo[0].width)
  ifile.write("A_space:=%.2f;\n"%imlo[0].space)
  ifile.write("A_spacept:=%.2fpt;\n"%imlo[0].space)
  ifile.write("A_xheight:=%.2f;\n"%imlo[0].xheight)
  ifile.write("A_capital:=%.2f;\n"%imlo[0].capital)
  ifile.write("A_ascender:=%.2f;\n"%imlo[0].ascender)
  ifile.write("A_descender:=%.2f;\n"%imlo[0].descender)
  ifile.write("A_inktrap:=%.2f;\n"%imlo[0].inktrap)
  ifile.write("A_stemcut:=%.2f;\n"%imlo[0].stemcut)
  ifile.write("A_skeleton#:=%.2fpt#;\n"%imlo[0].skeleton)
  ifile.write("A_superness:=%.2f;\n"%imlo[0].superness)
  ifile.write("A_over:=%.2fpt;\n"%imlo[0].over)
  
# local parameters B  
  imlo = list(get_localparam(mfg.cFont.idlocalB))

  ifile.write("B_px#:=%.2fpt#;\n"%imlo[0].px)
  ifile.write("B_width:=%.2f;\n"%imlo[0].width)
  ifile.write("B_space:=%.2f;\n"%imlo[0].space)
  ifile.write("B_xheight:=%.2f;\n"%imlo[0].xheight)
  ifile.write("B_capital:=%.2f;\n"%imlo[0].capital)
  ifile.write("B_ascender:=%.2f;\n"%imlo[0].ascender)
  ifile.write("B_descender:=%.2f;\n"%imlo[0].descender)
  ifile.write("B_inktrap:=%.2f;\n"%imlo[0].inktrap)
  ifile.write("B_stemcut:=%.2f;\n"%imlo[0].stemcut)
  ifile.write("B_skeleton#:=%.2fpt#;\n"%imlo[0].skeleton)
  ifile.write("B_superness:=%.2f;\n"%imlo[0].superness)
  ifile.write("B_over:=%.2fpt;\n"%imlo[0].over)

  ifile.write("\n") 
  ifile.write("input glyphs\n") 
  ifile.write("bye\n") 
  ifile.close()
  return None 


def buildfname ( filename ):
    try :
      basename,extension = filename.split('.')
    except :
           extension="garbage"
           basename=""
    return [basename,extension]

def ufo2mf():
  print "************",mfg.cFont.fontpath
  dirnamef1 = mfg.cFont.fontpath+mfg.cFont.fontna+"/glyphs"
  dirnamef2 = mfg.cFont.fontpath+mfg.cFont.fontnb+"/glyphs"
  dirnamep1 = mfg.cFont.fontpath+"glyphs"
 
  charlist1 = [f for f in os.listdir(dirnamef1) ]
  charlist2 = [f for f in os.listdir(dirnamef2) ]

  for ch1 in charlist1: 
    fnb,ext=buildfname (ch1)
    if ext in ["glif"] and ( fnb == mfg.cFont.glyphunic or mfg.cFont.timestamp == 0 ) :

      print "file",ch1
    
      try :
        filech1 = open(dirnamef1+"/"+ch1,'r')
        filech2 = open(dirnamef2+"/"+ch1,'r')
        newfile,extension = ch1.split('.')
        newfilename=newfile+".mf"
        commd2 = "python parser_pino_mono.py " +ch1 +" " +dirnamef1 +" " +dirnamef2 +" > " +dirnamep1 +"/" +newfilename
        os.system(commd2)
      except :
        print "error",dirnamef1+"/"+ch1
        print "error",dirnamef2+"/"+ch1
      continue
  
  mfg.cFont.timestamp=1
  return None

def writeGlyphlist():

  print "*** write glyphlist ***"
  ifile=open(mfg.cFont.fontpath+"glyphlist.mf","w")
 

  dirnamep1 = mfg.cFont.fontpath+"glyphs"
 
  charlist1 = [f for f in os.listdir(dirnamep1) ]

  for ch1 in charlist1: 
    fnb,ext=buildfname (ch1)
    if ext in ["mf"]  :

      ifile.write("input glyphs/"+ch1+"\n")
    
  ifile.close()
  return None


