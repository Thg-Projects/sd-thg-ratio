import random
import re
import traceback

import gradio as gr
import contextlib
from modules import script_callbacks, scripts, shared
from modules.shared import opts
import requests
import bs4
from bs4 import BeautifulSoup
from pathlib import Path
import json

# diretorio = scripts.basedir()
# file = Path(diretorio, "resolution.json")

def on_ui_settings():
	section = ('ratio-imagems', "ratio-imagems")

def calculate_new_dimensions(original_width, original_height, target_width=None, target_height=None):
	new_width = original_width
	new_height = original_height

	if target_width and target_height:
		if original_width / target_width > original_height / target_height:
			new_width = target_width
			new_height = original_height * target_width / original_width
		else:
			new_width = original_width * target_height / original_height
			new_height = target_height
	elif target_width:
		new_width = target_width
		new_height = original_height * target_width / original_width
	elif target_height:
		new_width = original_width * target_height / original_height
		new_height = target_height

	return {'width': round(new_width,0), 'height': round(new_height,0)}

# def teste():
# 	title, name, ratio, res_w, res_h = [], [], [], [], []  
# 	with open(f"{file}") as fileS:
# 		MYJSON = json.load(fileS)

# 	for i in MYJSON:
# 		title.append(i["title"])
# 		name.append(i["name"])
# 		ratio.append(i["ratio"])
# 		res_w.append(i["res_w"])
# 		res_h.append(i["res_h"])
# 	return title, name, ratio

def sentence_builder(radio,widthFix, heightFix, imagem):
	original_width = imagem.width
	original_height = imagem.height

	target_width = widthFix
	target_height = heightFix
	if radio == "Largura":
		target_width = int(widthFix)
		target_height = None
		print("lll")
	elif radio == "Altura":
		target_width = None
		target_height = int(heightFix)
		print("222")
	else:
		print("33")
		target_width = 512
		target_height = None
	


	new_dimensions = calculate_new_dimensions(int(original_width), int(original_height),target_width, target_height)

	# print(new_dimensions)



	html = (
		'<style>.row{display:flex;flex-wrap:wrap;gap:var(--size-4);width:var(--size-full)}.col.s6.trdd{display:flex;align-items:center;justify-content:center;font-size: 3em;}</style>'+
'         <div class="row">'+
	'    <div class="col s6">'+
'         Tamanho Original'+
'         <br><span class="textspan svelte-1m96bx3 hl" style="background-color: rgb(254, 226, 226);"> <span class="text svelte-1m96bx3">'+
'                 Largura'+
'             </span> &nbsp; <span class="label svelte-1m96bx3" style="background-color: rgb(220, 38, 38);">'+
					str(original_width) +' px'+
'             </span> </span><br><span class="textspan svelte-1m96bx3 hl" style="background-color: rgb(254, 226, 226);">'+
'             <span class="text svelte-1m96bx3">'+
'                 Altura'+
'              </span> &nbsp; <span class="label svelte-1m96bx3" style="background-color: rgb(220, 38, 38);">'+
str(original_height) +' px'+
'             </span>  </span></div>'+
'      <div class="col s6 trdd">=&gt;</div>'+
'     <div class="col s6">'+
'         Novo Tamanho'+
'         <br><span class="textspan svelte-1m96bx3 hl" style="background-color: rgb(220, 252, 231);"><span class="text svelte-1m96bx3">'+
'                  Width'+
'             </span> &nbsp; <span class="label svelte-1m96bx3" style="background-color: rgb(22, 163, 74);">'+
				str(new_dimensions["width"])+' px'+
'             </span> </span><br><span class="textspan svelte-1m96bx3 hl" style="background-color: rgb(219, 234, 254);">'+
'              <span class="text svelte-1m96bx3">'+
'                  Height'+
'               </span> &nbsp; <span class="label svelte-1m96bx3" style="background-color: rgb(37, 99, 235);">'+
str(new_dimensions["height"])+' px'+
'               </span> </span></div>'+
'  </div>        ' )
#    hl = [str(new_dimensions["width"]),str(new_dimensions["height"])]
#   return [('thg','123'),('sss',None)]
	# hl = [('ratio width',str(new_dimensions["width"])),('ratio height',str(new_dimensions["height"]))]
	# self.xxx = new_dimensions["width"]
	# self.yyy = new_dimensions["height"] 
	
	# hl = [('Tamanho Original ',None),('width',str(original_width)),('height',str(original_height)),(',novo tamanho com Ratio alterado =>',None),('ratio width',str(new_dimensions["width"])),('ratio height',str(new_dimensions["height"]))]
	return html,new_dimensions["width"],new_dimensions["height"]

def greet(name):
    return "Hello " + name + "!"

class BooruPromptsScript(scripts.Script):
	# def __init__(self) -> None:
	# 	super().__init__()

	def __init__(self, res=(512, 512), **kwargs):
		super().__init__(**kwargs)
		self.t2i_w, self.t2i_h = res
		
	def title(self):
		return("Proportion Ratio 1")
	def show(self, is_img2img):
		return scripts.AlwaysVisible

	def ui(self, is_img2img):
		with gr.Group():
			with gr.Accordion("Proportion Ratio", open=False):

				with gr.Blocks(css="#b1 {width: var(--size-16)}") as demo:
					# gr.Markdown("Flip text or image files using this demo.")
					with gr.Tab("Ratio Imagem"):
						with gr.Accordion(""):
							with gr.Row():
								with gr.Column(scale=1, min_width=300):
									img_input = gr.Image(type="pil",label="Imagem Proporção")                    

								with gr.Column(scale=1, min_width=200):     
									bt_radio = gr.Radio(["Largura", "Altura"], label="Escolha a proporção que deve ser alterada?")           
									with gr.Row():                        
										txt_width = gr.Number(value=512,label='Largura')
										txt_height = gr.Number(value=512,label='Altura')
									with gr.Row():
										bt_html =gr.HTML(label="Log proporção")   
										# text_id =gr.Textbox()
										# bt_w =gr.Button(value='512px',elem_id="b1")
										# bt_h =gr.Button(value='512px',elem_id="b2")
									
									# bt_json =gr.JSON()
									# bt_high =gr.HighlightedText( label="Novo Ratio" )     
								
							# ratio_button = gr.Button("nova Proporção")
							# gr.Markdown("Get Ratio...")
							text_button = gr.Button("nova Proporção")  
							# send_prompt_btnx = gr.Button(value="Send to txt2img and img2img", elem_id="thg")     
							
						
					with gr.Tab("Lista de Resoluções"):
						with gr.Row():
							     
							gr.Textbox()
								# for title, name, ratio in zip(teste()[0], teste()[1], teste()[2]):
								# 	name =gr.Button(value=name+"-"+title,elem_id=ratio).style(full_width=False)
									# name.click(greet, inputs=name, outputs=mytext) 
								# image_output = gr.Image()  
							gr.Markdown("Portraits")
						image_button = gr.Button("Flip")
		# send_prompt_btnx.click(sentence_builder, inputs=[bt_radio,txt_width,txt_height,img_input], outputs=[bt_html,self.t2i_w,self.t2i_h])
		with contextlib.suppress(AttributeError):							
			text_button.click(sentence_builder, inputs=[bt_radio,txt_width,txt_height,img_input], outputs=[bt_html,self.t2i_w,self.t2i_h])
		
	
		

	def after_component(self, component, **kwargs):
		if kwargs.get("elem_id") == "txt2img_width":
			self.t2i_w = component
		if kwargs.get("elem_id") == "txt2img_height":
			self.t2i_h = component

		if kwargs.get("elem_id") == "img2img_width":
			self.i2i_w = component
		if kwargs.get("elem_id") == "img2img_height":
			self.i2i_h = component
	    
script_callbacks.on_ui_settings(on_ui_settings)