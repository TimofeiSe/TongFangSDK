#!/usr/sbin/env python
# -*- coding: utf-8 -*-

import ctypes
from TongFangSDKdefines import *
from TongFangSDKstructs import *

#--- SDK CONNECTING ----------------------------------------------------------------------------------

tfs_NetSDK = ctypes.CDLL(r'tfcnetsdk.dll')
tfs_PlaySDK = ctypes.CDLL(r'tfcplaysdk.dll')

#--- EXCEPTIONS -------------------------------------------------------------------------------------------

class TFSdkError (Exception):
	# TFC_NET_API DWORD TFC_NET_GetLastError(void);
	TFC_NET_GetLastError_ = tfs_NetSDK.TFC_NET_GetLastError 
	TFC_NET_GetLastError_.restype = DWORD
	# TFC_NET_API char *TFC_NET_GetErrorMsg(LONG *pErrorNo);
	TFC_NET_GetErrorMsg_ = tfs_NetSDK.TFC_NET_GetErrorMsg
	TFC_NET_GetErrorMsg_.argtypes = [cPointerType(LONG)]
	TFC_NET_GetErrorMsg_.restype = PCHAR
	# TFC_NET_GetErrorMsg seems to not work, so:
	error_messages = {0: 'No error', 1: 'SDK No Initialization', 2: 'NET_COMMANDTIMEOUT', 3: 'Parameter error', 4: 'Allocate memory resources failed', 5: 'NET_FILEOPENFAIL', 6: 'Connect device failed', 7: 'NET_PLAYFAIL', 8: 'Create socket failed', 9: 'Create Socket failed', 10: 'Assigned registration number of connections exceeds system permission', 11: 'NET_SOCKETLISTEN_ERROR', 12: 'NET_WRITEFILE_FAILED', 13: 'Input dynamic link library error', 14: 'NET_DIR_ERROR', 15: 'Create file failed', 16: 'NET_OPERNOTFINISH', 17: 'Send data failed', 18: 'Create thread failed', 19: 'Can not find some function entry from PlaySDK', 20: 'Not login before preview', 21: 'Over SDK maximum number of video connection', 22: 'Create EVENT failed', 23: 'Receive data time-out', 24: 'User doesn’t exit. User ID registered has been logouted or is unavaiable', 25: 'Initialize winsock library failed', 26: 'NET_NO_VIDEOSOURCE', 27: 'NET_SENSOR_ERROR', 0x2000: 'NET_BAD_HEADLINE', 0x2001: 'NET_NOSUPPORT', 0x2002: 'NET_NOCONTENT', 0x2003: 'NET_ERRORDATA', 0x2004: 'NET_INVALID_CMD', 0x2005: 'NET_MAX_CONNECTION', 0x2006: 'NET_PRIVILEGE_INVALID', 0x2007: 'NET_INVALID_USER'}
	def __init__(self):
		last_error = self.TFC_NET_GetLastError_()
		# error_message = self.TFC_NET_GetErrorMsg_(cPointer(LONG(last_error)))
		error_message = self.error_messages.get(last_error, 'Unknown error')
		self.value = 'TongFang Error [%d]: %s' % (last_error, error_message)
	def __str__(self):
		return repr(self.value)
class TFNotImplementedError (Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)
		
		
#--- FUNCTIONS -------------------------------------------------------------------------------------------

# TFC_NET_API BOOL TFC_NET_Init();
def tfc_Init():
	tfc_Init_ = tfs_NetSDK.TFC_NET_Init; tfc_Init_.restype = BOOL
	if not tfc_Init_(): raise TFSdkError()
	return True

# TFC_NET_API BOOL TFC_NET_Cleanup();
def tfc_Cleanup():
	tfc_Cleanup_ = tfs_NetSDK.TFC_NET_Cleanup; tfc_Cleanup_.restype = BOOL
	if not tfc_Cleanup_(): raise TFSdkError()
	return True
	
#TFC_NET_API BOOL TFC_NET_GetLocalIP(char strIP[16][16], DWORD *pValidNum, BOOL pEnableBind);
def tfc_GetLocalIP():
	tfc_GetLocalIP_ = tfs_NetSDK.TFC_NET_GetLocalIP; tfc_GetLocalIP_.restype = BOOL
	strIP = (CHAR * 16 * 16)()
	dwValidNum, bEnableBind = DWORD(), BOOL()
	result = tfc_GetLocalIP_(strIP, cPointer(dwValidNum), bEnableBind)
	if not result: raise TFSdkError()
	return [strIP[i].value for i in range(dwValidNum.value)]

#TODO: Not implemented in SDK:
# TFC_NET_API BOOL TFC_NET_SetValidIP(DWORD dwIPIndex, BOOL bEnableBind);
	
#TFC_NET_API BOOL TFC_NET_SetConnectTime(DWORD dwWaitTime, DWORD dwTryTimes);
#TFC_NET_API BOOL TFC_NET_SetHeartBeat(DWORD dwWaitTime);
#TFC_NET_API BOOL TFC_NET_SetReconnect(DWORD dwInterval,  BOOL bEnableRecon);

#TODO: Why it doesn't work?
# TFC_NET_API BOOL TFC_NET_SearchUnits(char* szBuf, int nBufLen, int* pRetLen, DWORD dwSearchTime, char *szLocalIp);
def tfc_SearchUnits(local_ip=None):
	TFC_NET_SearchUnits_ = tfs_NetSDK.TFC_NET_SearchUnits; TFC_NET_SearchUnits_.restype = BOOL
	search_buffer = cCreateStr(cSizeof(DeviceInfo_t()))
	search_buffer_len = len(search_buffer)
	ret_len = INT()
	result = TFC_NET_SearchUnits_(
			search_buffer,
			search_buffer_len,
			ret_len,
			1000,
			local_ip or ''
		)
	if result: return search_buffer
	else: return None

# TFC_NET_API LONG TFC_NET_StartSearchUnits(fSearchUnitsCB cbSearch, DWORD dwUser, char* szLocalIp);
# 	void (CALLBACK *fSearchUnitsCB)(DeviceInfo_t *dinfo, DWORD dwUser);
def tfc_StartSearchUnits(cbSearch, user_id, local_ip=None):
	tfc_StartSearchUnits_ = tfs_NetSDK.TFC_NET_StartSearchUnits; tfc_StartSearchUnits_.restype = LONG
	# cbSearchFunction = tfc_fSearchUnitsCB(cbSearch)
	# search_id = tfc_StartSearchUnits_(cbSearchFunction, user_id, local_ip or '')
	search_id = tfc_StartSearchUnits_(cbSearch, user_id, local_ip or '')
	if search_id < 0: raise TFSdkError()
	return search_id
	
# TFC_NET_API BOOL TFC_NET_StopSearchUnits(LONG lSearchHandle);
def tfc_StopSearchUnits(search_id):
	tfc_StopSearchUnits_ = tfs_NetSDK.TFC_NET_StopSearchUnits; tfc_StopSearchUnits_.restype = BOOL
	# if tfc_StopSearchUnits_(LONG(search_id)): raise TFSdkError()
	if tfc_StopSearchUnits_(): raise TFSdkError()
	return True

#TODO: Not needed
# TFC_NET_API BOOL TFC_NET_GetIPByResolveSvr(char *pchIP, WORD wPort, BYTE *sName, WORD wDVRNameLen, BYTE *sSerialNumber, WORD wSerialLen, char* sGetIP);

# TFC_NET_API LONG TFC_NET_Login(UserLoginInfo_t *pUserLoginInfo, DeviceInfo_t *devInfo);
def tfc_Login(ip='192.168.1.188', port=1115, username='admin', password='admin'):
	tfc_Login_ = tfs_NetSDK.TFC_NET_Login; tfc_Login_.restype = LONG
	device_info = DeviceInfo_t()
	user_id = tfc_Login_(
			cPointer(UserLoginInfo_t(ip, port, username, password)), 
			cPointer(device_info))
	if user_id < 0: raise TFSdkError()
	return user_id, device_info

# TFC_NET_API BOOL TFC_NET_Logout(LONG lUserID);
def tfc_Logout(user_id):
	tfc_Logout_ = tfs_NetSDK.TFC_NET_Logout; tfc_Logout_.restype = BOOL
	if tfc_Logout_(user_id) < 0: raise TFSdkError()
	return True

# TODO: Add cbRealData, dwUser, block
# TFC_NET_API LONG TFC_NET_Realplay(LONG lUserID, TFC_REALPLAY *play, fRealDataCB cbRealData, DWORD dwUser, int block);
def tfc_RealPlay(user_id, channel=0):
	tfc_RealPlay_ = tfs_NetSDK.TFC_NET_Realplay; tfc_RealPlay_.restype = LONG
	play = TFC_REALPLAY(channel)
	play_id = tfc_RealPlay_(
			user_id, cPointer(play),
			None, None, 1
		)
	if play_id < 0: raise TFSdkError()
	return play_id
	
# TFC_NET_API BOOL TFC_NET_SetRealDataCallBack(LONG lRealHandle, fRealDataCB cbRealData, DWORD dwUser);
# TFC_NET_API BOOL TFC_NET_RegisterDrawFun(LONG lRealHandle, fDrawFun cbDraw, LONG nUser);
	
# TFC_NET_API BOOL TFC_NET_GetVideoInfo(LONG lRealHandle, VidMediaInfo_t *vinfo);
def tfc_GetVideoInfo(play_id):
	tfc_GetVideoInfo_ = tfs_NetSDK.TFC_NET_GetVideoInfo
	tfc_GetVideoInfo_.restype = BOOL
	video_info = VidMediaInfo_t()
	result = tfc_GetVideoInfo_(play_id, cPointer(video_info))
	if not result: raise TFSdkError()
	return video_info
	
# TFC_NET_API BOOL TFC_NET_GetAudioInfo(LONG lRealHandle, AudMediaInfo_t *ainfo);
def tfc_GetAudioInfo(play_id):
	tfc_GetAudioInfo_ = tfs_NetSDK.TFC_NET_GetAudioInfo
	tfc_GetAudioInfo_.restype = BOOL
	audio_info = AudMediaInfo_t()
	result = tfc_GetAudioInfo_(play_id, cPointer(audio_info))
	if not result: raise TFSdkError()
	return audio_info
	
# TFC_NET_API BOOL TFC_NET_GetVideoStatics(LONG lRealHandle, float *fps, float *bps);
def tfc_GetVideoStatics(play_id):
	tfc_GetVideoStatics_ = tfs_NetSDK.TFC_NET_GetVideoStatics
	tfc_GetVideoStatics_.restype = BOOL
	fps, bps = FLOAT(), FLOAT()
	result = tfc_GetVideoStatics_(play_id, cByref(fps), cByref(bps))
	if not result: raise TFSdkError()
	return {'fps': fps.value, 'bps': bps.value}
	
# TFC_NET_API BOOL TFC_NET_SetPlayBufferTime(LONG lRealHandle, LONG bufTime);
	
# TFC_NET_API BOOL TFC_NET_StopRealplay(LONG lRealHandle, int bBlock);
def tfc_StopRealPlay(play_id):
	tfc_StopRealPlay_ = tfs_NetSDK.TFC_NET_StopRealplay; tfc_StopRealPlay_.restype = BOOL
	result = tfc_StopRealPlay_(play_id, 0)
	if not result: raise TFSdkError()
	return True

#--- STOP HERE 20:46 16.07.2015 -----------------------------------------------------------------
# TFC_NET_API BOOL TFC_NET_PauseSound(LONG lRealHandle);
# TFC_NET_API BOOL TFC_NET_PlaySound(LONG lRealHandle);
# TFC_NET_API BOOL TFC_NET_SetVolume(LONG lRealHandle, LONG volume);
# TFC_NET_API LONG TFC_NET_GetVolume(LONG lRealHandle);








	
# TFC_NET_API BOOL TFC_NET_GetConfig(LONG lUserID, LONG cmd, LONG lChannel, LPVOID lpOutBuffer, DWORD dwOutBufferSize, LPDWORD lpBytesReturned, LONG lData, LONG fmtType, LONG timeout);
def tfc_GetConfig(user_id, command, channel=0, timeout=1000):
	out_buffers = {
			CMD_GET_NTP: NtpCfg_t, # 0
			CMD_GET_DEVICEINFO: DeviceInfo_t, # 2
			CMD_GET_DEVICESTATUS: DeviceStatus_t, # 3
			CMD_GET_TIME: TimeInfo_t, # 4
			CMD_GET_FTPCFG: FTPCfg_t, # 6
			CMD_GET_MJPEGCFG: ImgCfg_t, # 8
			CMD_GET_CAMERACFG: CameraCfg_t, # 10
			CMD_GET_MOTIONDETECT: MotionDetection_t, # 13
			CMD_GET_CAMERATAMPER: CameraTamper_t, # 15
			CMD_GET_SNAP_CFG: NET_SNAP_CFG, # 17
			CMD_GET_WIFI: Wifi_t, #WiFiCfg_t, # 19
			CMD_GET_SMTPCFG: MailCfg_t, # 23
			CMD_GET_DDNSCFG: DDNSCfg_t, # 25
			CMD_GET_VIDEOCODECCFG: VideoCodecCfg_t, # 29
			CMD_GET_AUDIOCODECCFG: AudioCfg_t, # 31
			CMD_GET_IPFILTERCFG: IPFilter_t, # 33
			CMD_GET_SERVERPORTS: ServerPorts_t, # 38
			CMD_GET_OSDCFG: OSDCfg_t, # 45
			CMD_GET_USERLIST: UserList_t, # 47
			CMD_GET_NETCFG: NetworkInterfaceList_t, # 55
			CMD_GET_VIDEOGLOBALCFG: VideoGlobalCfg_t, # 57
			CMD_GET_VIDEOOUTPUTCFG: VideoOutputCfg_t, # 59
			CMD_GET_UPLOAD: NET_UPLOAD_CFG, # 63
			CMD_GET_IO: NET_ALARM_IO_CFG, # 65
			CMD_GET_BOOT: NET_ALARM_BOOT_CFG, # 67
			CMD_GET_NETBROKEN: NET_ALARM_NETBROKEN_CFG # 69
			# Not implemented in SDK or what? :
			#	CMD_GET_DSTCFG = 40 #<
			#	CMD_GET_IOOUTCFG = 21 #< Get
			#	CMD_GET_LOGCFG = 49 #<
			#	CMD_GET_MULTICAST_CFG = 43 #<
			#	CMD_GET_PTZPROTOCOL = 35 #<
			#	CMD_GET_RECORD_CFG = 53 #<
			#	CMD_GET_REC_PACKET_CFG = 51 #<
			#	CMD_GET_SERIALPORTCFG = 27 #<
			#	CMD_GET_STORAGEDEVINFO = 42 #<
			#	CMD_GET_VIDEOEFFECT = 36 #<
			#	CMD_GET_VSPROTOCAL = 61 #<
		}
	channel_not_needed = [
			CMD_GET_NTP, 
			CMD_GET_DEVICEINFO, 
			CMD_GET_DEVICESTATUS, 
			CMD_GET_TIME, 
			CMD_GET_FTPCFG, 
			CMD_GET_CAMERACFG, 
			CMD_GET_MOTIONDETECT, 
			CMD_GET_CAMERATAMPER, 
			CMD_GET_SNAP_CFG, 
			CMD_GET_WIFI, 
			CMD_GET_SMTPCFG, 
			CMD_GET_DDNSCFG, 
			CMD_GET_IPFILTERCFG, 
			CMD_GET_SERVERPORTS, 
			CMD_GET_OSDCFG, 
			CMD_GET_USERLIST, 
			CMD_GET_NETCFG, 
			CMD_GET_VIDEOGLOBALCFG, 
			CMD_GET_VIDEOOUTPUTCFG, 
			CMD_GET_UPLOAD, 
			CMD_GET_IO, 
			CMD_GET_BOOT, 
			CMD_GET_NETBROKEN
		]
	if command not in out_buffers.keys():
		raise TFSdkNotImplementedError()
	if command in channel_not_needed:
		channel = 0
	tfc_GetConfig_ = tfs_NetSDK.TFC_NET_GetConfig; tfc_GetConfig_.restype = BOOL
	out_buffer = out_buffers[command]()
	bytes_returned, expand_data = DWORD(), LONG()
	format_type = LONG(0) # 0: binary, 1: xml
	timeout = LONG(timeout)
	result = tfc_GetConfig_( user_id, command, LONG(channel), cPointer(out_buffer), cSizeof(out_buffer), cPointer(bytes_returned), expand_data, format_type, timeout )
	if not result: raise TFSdkError()
	return out_buffer

def tfc_SetConfig(user_id, command, data_buffer, channel=0, timeout=1000):
	# TFC_NET_API BOOL TFC_NET_SetConfig(LONG   lUserID, LONG   cmd, LONG   lChannel, LPVOID lpInBuffer, DWORD  dwInBufferSize, LONG   cmdFlag, LONG   timeout);
	data_buffers = {
			CMD_SET_NTP: NtpCfg_t, # 1
			CMD_SET_TIME: TimeInfo_t, # 5
			CMD_SET_FTPCFG: FTPCfg_t, # 7
			CMD_SET_MJPEGCFG: ImgCfg_t, # 9
			CMD_SET_CAMERACFG: CameraCfg_t, # 11
			CMD_SET_PRIVACYMASK: PrivacyMask_t, # 12
			CMD_SET_MOTIONDETECT: MotionDetection_t, # 14
			CMD_SET_CAMERATAMPER: CameraTamper_t, # 16
			CMD_SET_SNAP_CFG: NET_SNAP_CFG, # 18
			CMD_SET_WIFI: Wifi_t, #WiFiCfg_t, # 20
			CMD_SET_SMTPCFG: MailCfg_t, # 24
			CMD_SET_DDNSCFG: DDNSCfg_t, # 26
			CMD_SET_VIDEOCODECCFG: VideoCodecCfg_t, # 30
			CMD_SET_AUDIOCODECCFG: AudioCfg_t, # 32
			CMD_SET_IPFILTERCFG: IPFilter_t, # 34
			CMD_SET_SERVERPORTS: ServerPorts_t, # 39
			CMD_SET_OSDCFG: OSDCfg_t, # 46
			CMD_SET_USERLIST: UserList_t, # 48
			CMD_SET_NETCFG: NetworkInterfaceList_t, # 56
			CMD_SET_VIDEOGLOBALCFG: VideoGlobalCfg_t, # 58
			CMD_SET_VIDEOOUTPUTCFG: VideoOutputCfg_t, # 60
			CMD_SET_UPLOAD: NET_UPLOAD_CFG, # 64
			CMD_SET_IO: NET_ALARM_IO_CFG, # 66
			CMD_SET_BOOT: NET_ALARM_BOOT_CFG, # 68
			CMD_SET_NETBROKEN: NET_ALARM_NETBROKEN_CFG # 70
			# Not implemented in SDK or what? :
			#	CMD_SET_DSTCFG = 41 #<
			#	CMD_SET_IOOUTCFG = 22 #< Set
			#	CMD_SET_LOGCFG = 50 #<
			#	CMD_SET_MULTICAST_CFG = 44 #<
			#	CMD_SET_RECORD_CFG = 54 #<
			#	CMD_SET_REC_PACKET_CFG = 52 #<
			#	CMD_SET_SERIALPORTCFG = 28 #<
			#	CMD_SET_VIDEOEFFECT = 37 #<
			#	CMD_SET_VSPROTOCAL = 62 #<
		}
	channel_not_needed = [
			CMD_SET_NTP, 
			CMD_SET_TIME, 
			CMD_SET_FTPCFG, 
			CMD_SET_PRIVACYMASK, 
			CMD_SET_MOTIONDETECT, 
			CMD_SET_CAMERATAMPER, 
			CMD_SET_SNAP_CFG, 
			CMD_SET_WIFI, 
			CMD_SET_SMTPCFG, 
			CMD_SET_DDNSCFG, 
			CMD_SET_IPFILTERCFG, 
			CMD_SET_SERVERPORTS, 
			CMD_SET_OSDCFG, 
			CMD_SET_USERLIST, 
			CMD_SET_NETCFG, 
			CMD_SET_VIDEOGLOBALCFG, 
			CMD_SET_VIDEOOUTPUTCFG, 
			CMD_SET_UPLOAD, 
			CMD_SET_IO, 
			CMD_SET_BOOT, 
			CMD_SET_NETBROKEN
		]
	if command not in data_buffers.keys():
		raise TFSdkNotImplementedError('TongFang ERROR: Command %s for SetConfig is not set command or not implmented' % command)
	if not type(data_buffer) == type(data_buffers[command]()):
		raise TFSdkNotImplementedError('TongFang ERROR: Command %s and data (%s) mismatch in SetConfig: '
			'data must be of type %s' % (command, type(data_buffer).__name__, type(data_buffers[command]()).__name__))
	channel = 0 if command in channel_not_needed else command
	tfc_SetConfig_ = tfs_NetSDK.TFC_NET_SetConfig; tfc_SetConfig_.restype = BOOL
	result = tfc_SetConfig_(user_id, command, channel, cPointer(data_buffer), cSizeof(data_buffer), 0, timeout)
	if not result: raise TFSdkError()
	return result


def tfc_Reboot(user_id):
	# TFC_NET_API LONG TFC_NET_Reboot(LONG lUserID);
	tfc_Reboot_ = tfs_NetSDK.TFC_NET_Reboot
	tfc_Reboot_.restype = LONG
	return not tfc_Reboot_(user_id)
	
def tfc_CaptureBMP(play_id, filename=None):
	#TFC_NET_API BOOL TFC_NET_CaptureBMP(LONG lRealHandle, const char *szFileName);
	tfc_CaptureBMP_ = tfs_NetSDK.TFC_NET_CaptureBMP
	tfc_CaptureBMP_.restype = BOOL
	filename = filename or 'Capture.bmp'
	result = tfc_CaptureBMP_(LONG(play_id), filename)
	if not result: raise TFSdkError()
	return result
	
def tfc_CaptureJPEG(play_id, filename=None, quality=5):
	#TFC_NET_API BOOL TFC_NET_CaptureJPEG(LONG lRealHandle, const char *szFileName, int iQuality);
	tfc_CaptureJPEG_ = tfs_NetSDK.TFC_NET_CaptureJPEG
	tfc_CaptureJPEG_.restype = BOOL
	filename = filename or 'Capture.jpg'
	result = tfc_CaptureJPEG_(play_id, filename, quality)
	if result < 0: raise TFSdkError()
	return result
	
def tfc_StartRecord(play_id, filename=None):
	#TFC_NET_API BOOL TFC_NET_StartRecord(LONG lRealHandle, const char *szFileName);
	tfc_StartRecord_ = tfs_NetSDK.TFC_NET_StartRecord
	tfc_StartRecord_.restype = BOOL
	filename = filename or 'Capture.avi'
	result = tfc_StartRecord_(play_id, filename)
	if not result: raise TFSdkError()
	return result
	
def tfc_StopRecord(play_id):
	#TFC_NET_API BOOL TFC_NET_StopRecord(LONG lRealHandle);
	tfc_StopRecord_ = tfs_NetSDK.TFC_NET_StopRecord
	tfc_StopRecord_.restype = BOOL
	result = tfc_StopRecord_(play_id)
	if not result: raise TFSdkError()
	return result
	
	

'''
//************************************
// Method:    TFC_NET_Restore
// FullName:  TFC_NET_Restore
// Returns:   TFC_NET_API BOOL
// Parameter: LONG lUserID
//************************************
TFC_NET_API BOOL TFC_NET_Restore(LONG lUserID);

//************************************
// Method:    TFC_NET_GetDeviceCaps
// FullName:  TFC_NET_GetDeviceCaps
// Returns:   BOOL
// Parameter: LONG lUserID
// Parameter: DWORD dwCapType
// Parameter: char  *pOutBuf
// Parameter: DWORD dwCapacity
// Parameter: DWORD *dwOutLength
// Parameter: DWORD fmtType
//************************************
TFC_NET_API BOOL TFC_NET_GetDeviceCaps(LONG   lUserID,
                                       DWORD  dwCapType,
                                       char   *pOutBuf,
                                       DWORD  dwCapacity,
                                       DWORD  *dwOutLength,
                                       DWORD  fmtType);

//************************************
// Method:    TFC_NET_AbatchSetIp
// FullName:  TFC_NET_AbatchSetIp
// Returns:   BOOL
// Parameter: char *szFirstIP
// Parameter: NetworkInterfaceList_t *pAbatchIfaceParam
// Parameter: ULONG deviceNnm
// Parameter: UserLoginInfo_t *pUserLoginInfo
// Parameter: char *szLocalIp
//************************************
TFC_NET_API BOOL TFC_NET_AbatchSetIp(char *szFirstIP, AbatchIPCfg_t *pAbatchIfaceParam, ULONG deviceNnm, UserLoginInfo_t *pUserLoginInfo, char *szLocalIp);
'''




'''
//************************************
// Method:    TFC_NET_SetConnectTime
// FullName:  TFC_NET_SetConnectTime
// Returns:   BOOL
// Parameter: DWORD dwWaitTime
// Parameter: DWORD dwTryTimes
//************************************
TFC_NET_API BOOL TFC_NET_SetConnectTime(DWORD dwWaitTime, DWORD dwTryTimes);

//************************************
// Method:    TFC_NET_SetConnectTime
// FullName:  TFC_NET_SetConnectTime
// Returns:   BOOL
// Parameter: DWORD dwWaitTime
//************************************
TFC_NET_API BOOL TFC_NET_SetHeartBeat(DWORD dwWaitTime);

//************************************
// Method:    TFC_NET_SetReconnect
// FullName:  TFC_NET_SetReconnect
// Returns:   TFC_NET_API BOOL
// Parameter: DWORD dwInterval
// Parameter: BOOL bEnableRecon
//************************************
TFC_NET_API BOOL TFC_NET_SetReconnect(DWORD dwInterval,  BOOL bEnableRecon);

//************************************
// Method:    TFC_NET_GetIPByResolveSvr
// FullName:  TFC_NET_GetIPByResolveSvr
// Returns:   BOOL
// Parameter: char * pchIP
// Parameter: WORD wPort
// Parameter: BYTE * sName
// Parameter: WORD wDVRNameLen
// Parameter: BYTE * sSerialNumber
// Parameter: WORD wSerialLen
// Parameter: char * sGetIP
//************************************
TFC_NET_API BOOL TFC_NET_GetIPByResolveSvr(char *pchIP, WORD wPort, BYTE *sName, WORD wDVRNameLen, BYTE *sSerialNumber, WORD wSerialLen, char* sGetIP);

'''







'''
//************************************
// Method:    TFC_NET_GetVideoStatics
// FullName:  TFC_NET_GetVideoStatics
// Returns:   BOOL
// Parameter: LONG lRealHandle
// Parameter: float * fps
// Parameter: float * bps
//************************************
TFC_NET_API BOOL TFC_NET_GetVideoStatics(LONG lRealHandle, float *fps, float *bps);

//************************************
// Method:    TFC_NET_GetPlayerIndex
// FullName:  TFC_NET_GetPlayerIndex
// Returns:   LONG
// Parameter: LONG lRealHandle
//************************************
TFC_NET_API LONG TFC_NET_GetPlayerIndex(LONG lRealHandle);

//************************************
// Method:    TFC_NET_GetWorkState
// FullName:  TFC_NET_GetWorkState
// Returns:   LONG
//************************************
TFC_NET_API LONG TFC_NET_GetWorkState(LONG lUserID);

//************************************
// Method:    TFC_NET_SetMDParam
// FullName:  TFC_NET_SetMDParam
// Returns:   BOOL
// Parameter: LONG   lUserID
// Parameter: ULONG   ulsensitivity
// Parameter: ULONG ulmvthreshold
// Parameter: ULONG  ulratio
// Parameter: LONG   timeout
//************************************
TFC_NET_API BOOL TFC_NET_SetMDParam(LONG   lUserID,
                                   ULONG   ulsensitivity,
                                   ULONG   ulmvthreshold,
                                   ULONG   ulratio,
                                   LONG   timeout);

//************************************
// Method:    TFC_NET_GetMDParam
// FullName:  TFC_NET_GetMDParam
// Returns:   BOOL
// Parameter: LONG   lUserID
// Parameter: ULONG   *pulsensitivity
// Parameter: ULONG   *pulmvthreshold
// Parameter: ULONG   *pulratio
// Parameter: LONG   timeout
//************************************
TFC_NET_API BOOL TFC_NET_GetMDParam(LONG   lUserID,
                                   ULONG   pulmvthreshold[10],
                                   ULONG   pulratio[10],
                                   LONG   timeout);
'''




#--- TFCPlaySDK ---------------------------------------------------------------------

def tfp_Init():
	#TFC_PLAY_API BOOL  TFCPlay_SDKInit();
	tfp_Init_ = tfs_PlaySDK.TFCPlay_SDKInit
	tfp_Init_.restype = BOOL
	result = tfp_Init_()
	if not result: raise TFSdkError()
	return bool(result)

def tfp_UnInit():
	#TFC_PLAY_API BOOL  TFCPlay_SDKUnInit();
	tfp_UnInit_ = tfs_PlaySDK.TFCPlay_SDKUnInit
	tfp_UnInit_.restype = BOOL
	result = tfp_UnInit_()
	if not result: raise TFSdkError()
	return bool(result)

def tfp_GetSdkVersion():
	#TFC_PLAY_API char *TFCPlay_GetSdkVersion();
	tfp_GetSdkVersion_ = tfs_PlaySDK.TFCPlay_GetSdkVersion
	tfp_GetSdkVersion_.restype = PCHAR
	result = tfp_GetSdkVersion_()
	if not result: raise TFSdkError()
	return str(result)

def tfp_GetPort():
	#TFC_PLAY_API BOOL  TFCPlay_GetPort(LONG *nPort);
	tfp_GetPort_ = tfs_PlaySDK.TFCPlay_GetPort
	tfp_GetPort_.restype = BOOL
	port = LONG()
	result = tfp_GetPort_(cPointer(port))
	if not result: raise TFSdkError()
	return port.value

def tfp_FreePort(port):
	#TFC_PLAY_API BOOL  TFCPlay_FreePort(LONG nPort);
	tfp_FreePort_ = tfs_PlaySDK.TFCPlay_FreePort
	tfp_FreePort_.restype = BOOL
	result = tfp_FreePort_(port)
	if not result: raise TFSdkError()
	return bool(result)

def tfp_GetLastError(port):
	#TFC_PLAY_API LONG  TFCPlay_GetLastError(LONG nPort);
	tfp_GetLastError_ = tfs_PlaySDK.TFCPlay_GetLastError
	tfp_GetLastError_.restype = LONG
	result = tfp_GetLastError_(port)
	if not result: raise TFSdkError()
	return long(result)

def tfp_OpenStream(port):
	#TFC_PLAY_API BOOL  TFCPlay_OpenStream(LONG nPort, PBYTE pFileHeadBuf, LONG nSize, LONG nBufPoolSize);
	tfp_OpenStream_ = tfs_PlaySDK.TFCPlay_OpenStream
	tfp_OpenStream_.restype = BOOL
	result = tfp_OpenStream_(port)
	if not result: raise TFSdkError()
	return bool(result)

def tfp_CloseStream(port):
	#TFC_PLAY_API BOOL  TFCPlay_CloseStream(LONG nPort);
	tfp_CloseStream_ = tfs_PlaySDK.TFCPlay_CloseStream
	tfp_CloseStream_.restype = BOOL
	result = tfp_CloseStream_(port)
	if not result: raise TFSdkError()
	return bool(result)






















#--- END ------------------------------------------------------------------------------------------

if __name__ == '__main__':
	tfc_Init()
	
	print 'local_ips:\n  %s\n' % '\n  '.join(tfc_GetLocalIP())
	
	user_id, device = tfc_Login('172.20.23.67')
	print 'user_id {0}\n  name {1.name}\n  serial {1.serial}\n  mac {1.macaddr}'.format(user_id, device)

	play_id = tfc_RealPlay(user_id)
	print 'play_id =', play_id
	video_info = tfc_GetVideoInfo(play_id)
	print '  vcodec {0.codec}\n  WxH {0.WxH}\n  fps {0.fps}'.format(video_info)
	audio_info = tfc_GetAudioInfo(play_id)
	print '  acodec {0.codec}\n  samplerate {0.samplerate}\n  bitrate {0.bitrate}\n  channels {0.channels}'.format(audio_info)
	print '  video statics', tfc_GetVideoStatics(play_id)
	
	print 'stop play =', tfc_StopRealPlay(play_id)
	
	tfc_Logout(user_id)
	
	tfc_Cleanup()
	print










