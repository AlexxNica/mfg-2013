""" Basic metafont point interface using webpy  """
import web
import model
import os
import sys
import glob 
### Url mappings

urls = (
    '/', 'Index',
    '/view/(\d+)', 'View',
    '/metap/(\d+)', 'Metap',
    '/viewfont/', 'ViewFont',
    '/font1/(\d+)', 'Font1',
    '/font2/(\d+)', 'GlobalParam',
)


### Templates
t_globals = {
    'datestr': web.datestr
}
render = web.template.render('templates', base='base', globals=t_globals)
###  classes



### preset font loading

class cFont:
     fontna = ""
     fontnb = ""
     fontname = ""
     idglobal = 1
     idmaster = '1'
     idwork   = '0'
     glyphName =""
     superness =1
     metapolation=0.5
     penwidth=1
     unitwidth=1
     xHeight=1
     
class Index:

    def GET (self):
        """ Show page """
        posts = model.get_posts()
        master = model.get_masters()
        fontsource = [cFont.fontna,cFont.fontnb,cFont.glyphName]
	webglyph = cFont.glyphName
        return render.metap(posts,master,fontsource,webglyph)


class Metap:

    def GET (self,id):
        """ Show page """
        cFont.idwork=id
        posts = model.get_posts()
        master = model.get_masters()
#        fontsource = [cFont.fontna,cFont.fontnb,cFont.glyphName]

        if id =='0':
#          we are working on font A
#
           fontsource = [cFont.fontna,cFont.glyphName]
        if id =='1':
#          we are working on font B
#          
           fontsource = [cFont.fontnb,cFont.glyphName]

	webglyph = cFont.glyphName
        return render.metap(posts,master,fontsource,webglyph)

class View:
    form = web.form.Form(
        web.form.Textbox('PointNr', web.form.notnull, 
            size=3,
            description="nr"),
        web.form.Textbox('x', web.form.notnull, 
            size=5,
            description="x"), 
        web.form.Textbox('y', web.form.notnull, 
            size=5,
            description="y"),
        web.form.Textbox('PointName',  
            size=5,
            description="name"),
        web.form.Button('save'), 
        )

    formParam = web.form.Form(
        web.form.Textbox('startp',
	    size=1,
            description="start"),
        web.form.Textbox('superness',
            size=4, 
            description="superness"),
 #       web.form.Dropdown(name='Cardinal',
 #           args=['Up', 'Left', 'Down', 'Right'],
#	    value='Up'),
        web.form.Dropdown(name='+ Parameter',
            args=['Tension', 'Direction', 'Line', 'Pen1', 'Pen2', 'Stem', 'Baseline', 'X-Height', 'Cap', 'Ascender', 'Descender']), 

#web.form.Checkbox('delete'), 
		
#            if Tension in args :
#               formParam = web.form.Form(
#               web.form.Textbox('Tension',
#               size=5, 
#               description="Tension"))

        web.form.Button('saveParam'), 
        )

   


    def GET(self,id):
        """ View single post """
        form=self.form()
        if id > '0' : 
           post = model.get_post(int(id))
           glyphparam = model.get_glyphparam(int(id))
           form.fill(post)
        posts = model.get_posts()
        formParam = self.formParam()
        if glyphparam != None :
           formParam.fill(glyphparam)
        mastglobal = model.get_globalparam(cFont.idglobal)
        master = model.get_master(cFont.idmaster)
	webglyph = cFont.glyphName
        return render.view(posts,post,form,formParam,master,mastglobal,webglyph)

    def POST(self, id):
        form = View.form()
        formParam = View.formParam()
        post = model.get_post(int(id))
        if not form.validates() :
            posts = model.get_posts()
            master = model.get_master(cFont.idmaster)
            mastglobal = model.get_globalparam(cFont.idglobal)
	    webglyph = cFont.glyphName
            return render.view(posts, post, form, formParam, master,mastglobal, webglyph)
        if form.d.PointName != None :
            if not formParam.validates() :
                return render.view(posts, post, form, formParam, master,mastglobal)
            if model.get_glyphparam(int(id)) != None :
                model.update_glyphparam(int(id),form.d.PointName, formParam.d.startp, formParam.d.superness)
            else :
                model.insert_glyphparam(int(id),form.d.PointName, formParam.d.startp, formParam.d.superness)
                
        model.update_post(int(id), form.d.x, form.d.y)
        posts = model.get_posts()
        master = model.get_master(cFont.idmaster)
        mastglobal = model.get_globalparam(cFont.idglobal)
	webglyph = cFont.glyphName

        model.writexml()        
        commstr = "python ufo2mf.py " + cFont.fontna+"/glyphs " + cFont.fontnb+"/glyphs glyphs"
	print commstr
        os.system(commstr)
        os.system("sh makefont.sh")
        return render.view(posts, post, form, formParam, master, mastglobal,webglyph)

class ViewFont:
    def GET(self):
        """ View single post """
        param=cFont.glyphName
        return render.viewfont(param)

class Font1:
    form = web.form.Form(
        web.form.Textbox('UFO_A', web.form.notnull, 
            size=20,
#            description="namea", value="oswald.ufo"),
            description="namea", value=cFont.fontna),
        web.form.Textbox('UFO_B', web.form.notnull, 
            size=20,
            description="nameb", value=cFont.fontnb),
        web.form.Textbox('GLYPH', web.form.notnull, 
            size=5,
            description="glyph", value="c"),
        web.form.Button('savefont'),
        )
    def GET(self,id):
        mmaster= list(model.get_masters())
        if id > '0' : 
           master= list(model.get_master(id))
        fontna = cFont.fontna
        fontnb = cFont.fontnb
        fontlist = [f for f in glob.glob("*.ufo")]
        form=self.form()
        form=Font1.form()
        form.fill({'UFO_A':fontna,'UFO_B':fontnb,'GLYPH':cFont.glyphName})
        return render.font1(fontlist,form,mmaster,cFont)

    def POST (self,id):
        mmaster= list(model.get_masters())
        master= list(model.get_master(id))
        form = Font1.form()
        form.fill()
        cFont.fontna = form.d.UFO_A
        cFont.fontnb = form.d.UFO_B
        cFont.glyphName  = form.d.GLYPH
        model.putFont()
        fontlist = [f for f in glob.glob("*.ufo")]
        return render.font1(fontlist,form,mmaster,cFont)

class GlobalParam:

    form = web.form.Form(
        web.form.Textbox('superness', web.form.notnull, 
            size=3,
            description="superness", value="1"),
        web.form.Textbox('metapolation', web.form.notnull, 
            size=3,
            description="metapolation", value="0.5"),
        web.form.Textbox('penwidth', web.form.notnull, 
            size=3,
            description="penwidth", value="1.0"),
        web.form.Textbox('unitwidth', web.form.notnull, 
            size=3,
            description="unitwidth", value="1.0"),
        web.form.Textbox('xHeight', web.form.notnull, 
            size=3,
            description="xHeight", value="1.0"),
        web.form.Button('save'),
        )
    def GET(self,id):
        
        gml = list(model.get_globalparams())
        form = self.form()
        if id > '0' :
          gm = list(model.get_globalparam(id))
        else:
          gm = None

        if gm != None:
             form.fill({'superness':gm[0].superness,'metapolation':gm[0].metapolation,'penwidth':gm[0].penwidth,'unitwidth':gm[0].unitwidth,'xHeight':gm[0].xHeight})
        return render.font2(form,gml,cFont)

    def POST (self,id):
        gml = list(model.get_globalparams())
        gm = list(model.get_globalparam(id))
        form = GlobalParam.form()
        form.fill()
        model.update_globalparam(id, form.d.superness, form.d.metapolation, form.d.penwidth, form.d.unitwidth, form.d.xHeight)
        model.writeGlobalParam()
        return render.font2(form,gml,cFont)

app = web.application(urls, globals())

if __name__ == '__main__':
    app.run()


app = web.application(urls, globals())

if __name__ == '__main__':
    app.run()

