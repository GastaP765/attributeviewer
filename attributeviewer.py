import maya.cmds as mc

def setAt(*args):
	global obj 

	sat = list(range(0))
	obj = mc.ls(sl=True)
	for i in obj:
		b = mc.listAttr(i, k=True)
		for f in b:
			sat.append('{0}.{1}'.format(i, f))
		sat.append('---------------')
	
	mc.textScrollList(tsl1, e=True, ra=True, append=sat)

def removeitem(*args):
	mc.textScrollList(tsl2, e=True, ra=True)

def addBr(*args):
	a = mc.textScrollList(tsl1, q=True, si=True)
	c = mc.textScrollList(tsl2, q=True, ai=True)
	while True:
		if '---------------' in a:
			a.remove('---------------')
		else:
			break

	if c is not None:
		for i in c:
			if i in a:
				a.remove(i)
	mc.textScrollList(tsl2, e=True, append=a)

def cutBr(*args):
	a = mc.textScrollList(tsl2, q=True, si=True)
	mc.textScrollList(tsl2, e=True, ri=a)

def ccUi(*args):
	lst = []
	chk = []
	hgt = 0
	k = 0
	a = mc.textScrollList(tsl2, q=True, ai=True)
	for i in range(len(obj)):
		hgt = hgt + 30
		b = []
		for f in a:
			if obj[i] in f:
				hgt = hgt + 30
				b.append(f)
				if obj[i] not in chk:
					chk.append(obj[i])
		
		lst.append(b)
	if mc.window('ccWindow', exists=True):
		mc.deleteUI('ccWindow')

	if hgt < 300:
		win = mc.window('ccWindow', t='ccWindow', widthHeight=(410, hgt))
		mc.window('ccWindow', e=True, widthHeight=(410, hgt))
	else:
		win = mc.window('ccWindow', t='ccWindow', widthHeight=(410, 300))
		mc.window('ccWindow', e=True, widthHeight=(410, 300))
	mc.scrollLayout(vst=16)
	mc.columnLayout()
	for i in lst:
		if len(i) != 0:
			c = i[0]
		else:
			continue
		d = c.split('.')
		# mc.scrollLayout(vst=16)
		mc.frameLayout(l=d[0])
		for j in i:
			e = j.split('.')
			tp = mc.getAttr(j, typ=True)
			g = mc.getAttr(j)
			if '{}'.format(tp) == 'doubleLinear':
				mc.floatSliderGrp('flt{}'.format(k), l=e[1], field=True, min=-10.0, max=10.0, fmn=-10000.0, fmx=10000.0, v=g)
			if '{}'.format(tp) == 'doubleAngle':
				mc.floatSliderGrp('flt{}'.format(k), l=e[1], field=True, min=-180.0, max=180.0, fmn=-3600.0, fmx=3600.0, v=g)
			elif '{}'.format(tp) == 'double':
				if 'scale' in '{}'.format(e[1]):
					mc.floatSliderGrp('flt{}'.format(k), l=e[1], field=True, min=0.0, max=10.0, fmn=0.0, fmx=10000.0, v=g)
				else:
					mc.floatSliderGrp('flt{}'.format(k), l=e[1], field=True, min=0.0, max=1.0, fmn=0.0, fmx=1.0, v=g)
			elif '{}'.format(tp) == 'bool':
				mc.floatSliderGrp('flt{}'.format(k), l=e[1], field=True, min=0, max=1, fmn=0, fmx=1, v=g)
			mc.connectControl('flt{}'.format(k), '{}'.format(j))
			k+=1

	mc.showWindow(win)

def mainWin():
	global tsl1, tsl2
	if mc.window('ATV', exists=True):
		mc.deleteUI('ATV')

	win = mc.window('ATV', t='AttributeViewer', mxb=False, s=False, widthHeight=(580,485))
	mc.window('ATV', e=True, widthHeight=(580,485))
	form = mc.formLayout()
	fl1 = mc.button(l='Select Attribute/Get Attribute', w=250, h=20, c=setAt)
	fl2 = mc.button(l='Browse Attribute/All Remove', w=250, h=20, c=removeitem)
	tsl1 = mc.textScrollList('tsl1', w=250, h=400, ams=True)
	tsl2 = mc.textScrollList('tsl2', w=250, h=400, ams=True)
	b1 = mc.button(l='>>', c=addBr, w=50, h=20)
	b2 = mc.button(l='<<', c=cutBr, w=50, h=20)
	b3 = mc.button(l='done', c=ccUi, w=560, h=30)

	mc.formLayout(form, e=True, af=[
		(fl1, 'top', 10), (fl1, 'left', 10),
		(fl2, 'top', 10), (fl2, 'left', 320)
	])
	mc.formLayout(form, e=True, af=[
		(tsl1, 'top', 35), (tsl1, 'left', 10),
		(tsl2, 'top', 35), (tsl2, 'left', 320)
	])
	mc.formLayout(form, e=True, af=[
		(b1, 'top', 210), (b1, 'left', 265),
		(b2, 'top', 240), (b2, 'left', 265),
		(b3, 'top', 445), (b3, 'left', 10),
	])

	mc.showWindow(win)

def consoleKey():
	mainWin()

consoleKey()