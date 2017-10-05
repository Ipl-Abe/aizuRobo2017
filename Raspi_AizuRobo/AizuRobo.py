#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

"""
 @file AizuRobo.py
 @brief ModuleDescription
 @date $Date$
"""
import sys
import time
sys.path.append(".")

# Import RTM module
import RTC
import OpenRTM_aist

import smbus
from time import sleep
import threading
import RPi.GPIO as GPIO
import math

# Import Service implementation class
# <rtc-template block="service_impl">

# </rtc-template>

# Import Service stub modules
# <rtc-template block="consumer_import">
# </rtc-template>


# This module's spesification
# <rtc-template block="module_spec">
aizurobo_spec = ["implementation_id", "AizuRobo", 
		 "type_name",         "AizuRobo", 
		 "description",       "ModuleDescription", 
		 "version",           "1.0.0", 
		 "vendor",            "UniversityofAizu", 
		 "category",          "Category", 
		 "activity_type",     "STATIC", 
		 "max_instance",      "1", 
		 "language",          "Python", 
		 "lang_type",         "SCRIPT",
		 ""]
# </rtc-template>

##
# @class AizuRobo
# @brief ModuleDescription
# 
# 
class AizuRobo(OpenRTM_aist.DataFlowComponentBase):
	
	##
	# @brief constructor
	# @param manager Maneger Object
	# 
	def __init__(self, manager):
		OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

		Button_arg = [None] * ((len(RTC._d_TimedULong) - 4) / 2)
		self._d_Button = RTC.TimedULong(*Button_arg)
		"""
		"""
		self._ButtonIn = OpenRTM_aist.InPort("Button", self._d_Button)
		Analog_arg = [None] * ((len(RTC._d_TimedDoubleSeq) - 4) / 2)
		self._d_Analog = RTC.TimedDoubleSeq(*Analog_arg)
		"""
		"""
		self._AnalogIn = OpenRTM_aist.InPort("Analog", self._d_Analog)


		


		# initialize of configuration-data.
		# <rtc-template block="init_conf_param">
		
		# </rtc-template>


		 
	##
	#
	# The initialize action (on CREATED->ALIVE transition)
	# formaer rtc_init_entry() 
	# 
	# @return RTC::ReturnCode_t
	# 
	#
	def onInitialize(self):
		# Bind variables and configuration variable
		
		# Set InPort buffers
		self.addInPort("Button",self._ButtonIn)
		self.addInPort("Analog",self._AnalogIn)
		


		#python　i2c通信用モジュール
		self.bus = smbus.SMBus(1)
		self.LEFTMOTOR_ADDRESS = 0x63  #左モータアドレス
		self.RIGHTMOTOR_ADDRESS = 0x64 #右モータアドレス
		self.CONTROL = 0x00			   #コントロールアドレス
		#モーター回転方向 0 : スタンバイ状態, 1 : 正転, 2: 逆転, 3: ブレーキ
		self.TOWARD_A = 0x00
		self.TOWARD_B = 0x00
		# Set OutPort buffers
		
		# Set service provider to Ports
		
		# Set service consumers to Ports
		
		# Set CORBA Service Ports
		
		#self._d_Analog.data.length(11)
		self.Aval = []
		self.Button = 0
		return RTC.RTC_OK
	
		##
		# 
		# The finalize action (on ALIVE->END transition)
		# formaer rtc_exiting_entry()
		# 
		# @return RTC::ReturnCode_t
	
		# 
	def onFinalize(self):
	
		return RTC.RTC_OK
	
		##
		#
		# The startup action when ExecutionContext startup
		# former rtc_starting_entry()
		# 
		# @param ec_id target ExecutionContext Id
		#
		# @return RTC::ReturnCode_t
		#
		#
	def onStartup(self, ec_id):
	
		return RTC.RTC_OK
	
		##
		#
		# The shutdown action when ExecutionContext stop
		# former rtc_stopping_entry()
		#
		# @param ec_id target ExecutionContext Id
		#
		# @return RTC::ReturnCode_t
		#
		#
	def onShutdown(self, ec_id):
	
		return RTC.RTC_OK
	
		##
		#
		# The activated action (Active state entry action)
		# former rtc_active_entry()
		#
		# @param ec_id target ExecutionContext Id
		# 
		# @return RTC::ReturnCode_t
		#
		#
	def onActivated(self, ec_id):
		#for i in range(11):
		#	self._d_Analog.data(i) = 0;
		return RTC.RTC_OK
	
		##
		#
		# The deactivated action (Active state exit action)
		# former rtc_active_exit()
		#
		# @param ec_id target ExecutionContext Id
		#
		# @return RTC::ReturnCode_t
		#
		#
	def onDeactivated(self, ec_id):
		
		#モータをスタンバイ状態に設定
		self.bus.write_i2c_block_data(self.LEFTMOTOR_ADDRESS,self.CONTROL,[0x00])
		self.bus.write_i2c_block_data(self.RIGHTMOTOR_ADDRESS,self.CONTROL,[0x00])

		return RTC.RTC_OK
	
		##
		#
		# The execution action that is invoked periodically
		# former rtc_active_do()
		#
		# @param ec_id target ExecutionContext Id
		#
		# @return RTC::ReturnCode_t
		#
		#

	#モータ指令値生成用関数 モーター指令値は (-100 ~ 100) の間で指定する.
	#i2c用通信byte変換前処理
	def map(self, x, in_min, in_max, out_min, out_max):

		#制御値
		value =0
		toward = 0x00

		if x > 0 : 　　　#正転
			toward = 1
			value = x

		elif x < 0 : 　　#逆転
			toward = 2
			value = abs(x)

		else : 　　　　　　　#停止時		
			value =0
			toward = 0
		
		return (value - in_min) * (out_max - out_min) // (in_max - in_min) + out_min, toward

	#アナログスティックの値変換関数
	def speedDetector(self, y, x):

		#停止
		if math.fabs(y) <= 0.2 and math.fabs(x) <= 0.2:
			Aval = 0.0
			Bval = 0.0
		else :
			pass
		#前進
		if  -0.2 < y and 0.2 < x and x < -0.2:
			Aval = -y * 50
			Bval = -y * 50
		else:
			pass
		#後退
		if   0.2 < y and 0.2 < x and x < -0.2:
			Aval = y * 50
			Bval = y * 50
		else:
			pass
		#左旋回
		if  -0.2 < y and y < 0.2 and x < -0.2:
			Aval = -x * 50
			Bval =  x * 50
		else:
			pass
		#右旋回
		if  -0.2 < y and y < 0.2 and 0.2 < x :
			Aval =  x * 50
			Bval = -x * 50
		else:
			pass



		return Aval, Bval

	def onExecute(self, ec_id):



		if self._AnalogIn.isNew():
			print "resultIn"
			indata = self._AnalogIn.read()
			#val = indata.data[0]
			
			#十字キー値
			POV_X = indata.data[0]
			POV_Y = indata.data[1]
			
			#左スティックアナログ値
			Ly = indata.data[2]
			Lx = indata.data[3]

			#右スティックアナログ値
			Ry = indata.data[4]
			Rx = indata.data[5]



			#Aval = math.sqrt((Ly*Ly + Lx+Lx))
			#Bval = math.sqrt((Ly*Ly + Lx+Lx))

			#コントローラ値変換作業

			Aval , Bval = self.speedDetector(Lx,Ly)



			s_A, self.TOWARD_A  = self.map(Aval , 0, 150, 0, 58)
			sval_A = self.TOWARD_A |((int(s) + 5) << 2)

			if sval_A >= 1 and sval_A <= 255  :
				self.bus.write_i2c_block_data(self.LEFTMOTOR_ADDRESS,self.CONTROL,[sval_A])
			else :
				print "DCmotor1 value limite "+str(sval_A)


			s_B, self.TOWARD_B  = self.map(Bval , 0, 150, 0, 58)
			sval_B = self.TOWARD_B |((int(s) + 5) << 2)

			if sval_B >= 1 and sval_B <= 255  :
				self.bus.write_i2c_block_data(self.LEFTMOTOR_ADDRESS,self.CONTROL,[sval_B])
			else :
				print "DCmotor1 value limite "+str(sval_B)


			#print "data : ", val
		else:
			pass
		if self._ButtonIn.isNew():
			print "buttonresult"
			buttondata = self._ButtonIn.read()
			button = buttondata.data
			print"button : ", button
		else:
			pass
		return RTC.RTC_OK
	
		##
		#
		# The aborting action when main logic error occurred.
		# former rtc_aborting_entry()
		#
		# @param ec_id target ExecutionContext Id
		#
		# @return RTC::ReturnCode_t
		#
		#
	def onAborting(self, ec_id):
	
		return RTC.RTC_OK
	
		##
		#
		# The error action in ERROR state
		# former rtc_error_do()
		#
		# @param ec_id target ExecutionContext Id
		#
		# @return RTC::ReturnCode_t
		#
		#
	def onError(self, ec_id):
	
		return RTC.RTC_OK
	
		##
		#
		# The reset action that is invoked resetting
		# This is same but different the former rtc_init_entry()
		#
		# @param ec_id target ExecutionContext Id
		#
		# @return RTC::ReturnCode_t
		#
		#
	def onReset(self, ec_id):
	
		return RTC.RTC_OK
	
		##
		#
		# The state update action that is invoked after onExecute() action
		# no corresponding operation exists in OpenRTm-aist-0.2.0
		#
		# @param ec_id target ExecutionContext Id
		#
		# @return RTC::ReturnCode_t
		#

		#
	def onStateUpdate(self, ec_id):
	
		return RTC.RTC_OK
	
		##
		#
		# The action that is invoked when execution context's rate is changed
		# no corresponding operation exists in OpenRTm-aist-0.2.0
		#
		# @param ec_id target ExecutionContext Id
		#
		# @return RTC::ReturnCode_t
		#
		#
	def onRateChanged(self, ec_id):
	
		return RTC.RTC_OK
	



def AizuRoboInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=aizurobo_spec)
    manager.registerFactory(profile,
                            AizuRobo,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    AizuRoboInit(manager)

    # Create a component
    comp = manager.createComponent("AizuRobo")

def main():
	mgr = OpenRTM_aist.Manager.init(sys.argv)
	mgr.setModuleInitProc(MyModuleInit)
	mgr.activateManager()
	mgr.runManager()

if __name__ == "__main__":
	main()
