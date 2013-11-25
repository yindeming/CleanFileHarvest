; Works for some installers

#include <Array.au3>
#include <Constants.au3>
#include <WinAPI.au3>

_Main()
Exit

Func _Main()
	Local $iPID = Run("installer.exe")

	Sleep(5000)

	Local $aWinList = WinList(); Get list of windows
	Local $hwnds[1], $p
	Local $avChildren

	; Get hwnds with titles from process list
	Local $i
	For $i = 1 To $aWinList[0][0]
		; Only display visble windows that have a title
		If $aWinList[$i][0] <> "" And IsVisible($aWinList[$i][1]) Then
			ReDim $hwnds[$p + 1]
			$hwnds[$p] = WinGetHandle($aWinList[$i][1])
			$p += 1
			;MsgBox(0, "Details", "Title=" & $aWinList[$i][0] & @LF & "Handle=" & $aWinList[$i][1])
		EndIf
	Next

	;_ArrayDisplay($hwnds)

	For $k = 0 To UBound($hwnds, 1) - 1
		;MsgBox(0, "", "hwnd is" & $hwnds[$k])
		WinListChildren($hwnds[$k], $avChildren)
		FindButton($avChildren)
	Next

EndFunc

Func IsVisible($handle);Check if the title is visible
    If BitAND(WinGetState($handle), 2) Then
        Return 1
    Else
        Return 0
    EndIf
EndFunc   ;==>IsVisible

; http://www.autoitscript.com/forum/topic/98583-list-all-child-controls-of-a-given-window/
Func WinListChildren($hwnd, ByRef $avArr)
	;If the array doesn't exist, we make a guess
    If UBound($avArr, 0) <> 2 Then ; Ubound - Returns the size of array dimensions: UBound ( Array [, Dimension(optional)] ). 2 = Array dimension is invalid.
        Local $avTmp[10][2] = [[0]]
        $avArr = $avTmp
    EndIf

    Local $hChild = _WinAPI_GetWindow($hwnd, $GW_CHILD)

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

;Func FindRadioButton()
;-I accept
;-I agree
;later

Func FindButton(ByRef $avChildren)
	Local $clickable[9] = ["", "Yes", "&Next >", "OK", "Continue", "Accept", "Agree", "Finish", "Install"]

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

