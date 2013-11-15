#include <Array.au3>
#include <Constants.au3>
#include <WinAPI.au3>

Global $avChildren

_Main()
Exit

Func _Main()
	; Run installer.exe and get its pid
	Local $pid = Run("installer.exe")

	;MsgBox(4096, "PID is", $pid)

	Sleep(2000)

	; Try to find slient switch
	;SilentInstall()

	;; List all the handles
	$hWnd = WinGetHandle("Setup")
	WinListChildren($hWnd, $avChildren)

	; Display the array
	;_ArrayDisplay($avChildren)

	; Try to search wanted button in $avChildren
	FindButton($avChildren)

EndFunc  ;==>_Main

;Func SilentInstall()
;	Run("ussf.exe installer.exe")
;EndFunc

; http://www.autoitscript.com/forum/topic/98583-list-all-child-controls-of-a-given-window/
Func WinListChildren($hWnd, ByRef $avArr)
	;If the array doesn't exist, we make a guess
    If UBound($avArr, 0) <> 2 Then ; Ubound - Returns the size of array dimensions: UBound ( Array [, Dimension(optional)] ). 2 = Array dimension is invalid.
        Local $avTmp[10][2] = [[0]]
        $avArr = $avTmp
    EndIf

    Local $hChild = _WinAPI_GetWindow($hWnd, $GW_CHILD)

    While $hChild
        If $avArr[0][0]+1 > UBound($avArr, 1)-1 Then ReDim $avArr[$avArr[0][0]+10][2] ;ReDim - Resize an existing array: ReDim $array[subscript 1]...[subscript n]
        $avArr[$avArr[0][0]+1][0] = $hChild
        $avArr[$avArr[0][0]+1][1] = _WinAPI_GetWindowText($hChild)
        $avArr[0][0] += 1
        WinListChildren($hChild, $avArr)
        $hChild = _WinAPI_GetWindow($hChild, $GW_HWNDNEXT)
    WEnd

    ReDim $avArr[$avArr[0][0]+1][2]
EndFunc

Func FindButton(ByRef $avChildren)
	Local $clickable[9] = ["", "Yes", "&Next", "OK", "Continue", "Accept", "Agree", "Finish", "Install"]

	While 1
		Local $i
		For $i = 1 To UBound($avChildren, 1) - 1
			Local $j
			For $j = 1 To UBound($clickable, 1) - 1
				If $avChildren[$i][1] <> "" And _
						$avChildren[$i][1] = $clickable[$j] Or _
						StringInStr($avChildren[$i][1], $clickable[$j]) Or _
						StringInStr($clickable[$j], $avChildren[$i][1]) Then
					ControlClick("", "", $avChildren[$i][0])
					ExitLoop
				EndIf
			Next
		Next
	WEnd

EndFunc

