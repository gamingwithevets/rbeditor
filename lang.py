import sys
if __name__ == '__main__':
	print('Please run main.py to start the program!')
	sys.exit()

lang = {
	'en_US': {
		'title': 'RECYCLE BIN EDITOR - RBEditor',
		'title_dtformat': 'Date and time formatting',
		'dtformat': 'Date and time format',
		'dtformat_preview': 'What your date and time format looks like when used:',
		'dtformat_guide': '''\
Source: https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes

%a - Weekday as locale’s abbreviated name.
%A - Weekday as locale’s full name.
%w - Weekday as a decimal number, where 0 is Sunday and 6 is Saturday.

%d - Day of the month as a zero-padded decimal number.
%b - Month as locale’s abbreviated name.
%B - Month as locale’s full name.
%m - Month as a zero-padded decimal number.
%y - Year without century as a zero-padded decimal number.
%Y - Year with century as a decimal number.

%H - Hour (24-hour clock) as a zero-padded decimal number.
%I - Hour (12-hour clock) as a zero-padded decimal number.
%p - Locale’s equivalent of either AM or PM.
%M - Minute as a zero-padded decimal number.
%S - Second as a zero-padded decimal number.
%f - Microsecond as a decimal number, zero-padded to 6 digits.
%z - UTC offset in the form '±HHMM[SS[.ffffff]]'.
%Z - Time zone name.

%j - Day of the year as a zero-padded decimal number.
%U - Week number of the year (Sunday as the first day of the week) as a zero-padded decimal number. All days in a new year preceding the first Sunday are considered to be in week 0.
%W - Week number of the year (Monday as the first day of the week) as a zero-padded decimal number. All days in a new year preceding the first Monday are considered to be in week 0.

%c - Locale’s appropriate date and time representation.
%x - Locale’s appropriate date representation.
%X - Locale’s appropriate time representation.

%G - ISO 8601 year with century representing the year that contains the greater part of the ISO week (%V).
%u - ISO 8601 weekday as a decimal number where 1 is Monday.
%V - ISO 8601 week as a decimal number with Monday as the first day of the week. Week 01 is the week containing Jan 4.

%% - A literal '%' character.

If you have used a Linux distribution you should be familiar with this process.\
''',

		'bytes': 'bytes',

		'menubar_file': 'File',
		'menubar_file_exit': 'Exit',
		'menubar_edit': 'Edit',
		'menubar_edit_reload': 'Reload Recycle Bin',
		'menubar_settings': 'Settings',
		'menubar_settings_dtformat': 'Date and time formatting...',
		'menubar_settings_language': 'Language',
		'menubar_settings_language_system': 'System Language',
		'menubar_help_update': 'Check for updates',
		'menubar_help_about': 'About ',

		'msgbox_error': 'Error',
		'msgbox_warning': 'Warning',
		'msgbox_no_formatting': 'This string has no formatting. Continue anyway?',
		'msgbox_blank': 'This string cannot be blank!',
		'msgbox_discard': 'Are you sure you want to discard your changes?',
		'msgbox_error_incorrect_fnamelen': 'Incorrect file name length in file',
		'msgbox_error_unsupported_version': 'Unknown or unsupported metadata file version',
		'msgbox_n_a': 'Not implemented',
		'msgbox_n_a_desc': 'This feature is not yet implemented into ',
		'msgbox_n_a_desc2': 'Sorry',
		'msgbox_setting_change': 'The program will now restart.\nAny unsaved changes will be lost.',
		'msgbox_not_in_rb': 'This item is no longer in the Recycle Bin.\nIt will now be removed from this list.',
		'msgbox_folder_warn': 'When opening a folder in the Recycle Bin, you cannot open any subfolders until the folder is restored.\n\nDo you want to continue?',
		'msgbox_lnk_warn': '''\
The file you opened was a shortcut file (.lnk).

If the file or folder this shortcut links to doesn't exist anymore, Windows will show a prompt asking if you want to delete the shortcut.
If you select Yes, the shortcut will be PERMANENTLY DELETED from the Recycle Bin.

If you opened the shortcut by accident, no need to fear, just press No.

Do you want to continue?\
''',
		'msgbox_restore': 'Restore this item?',
		'msgbox_restore_desc': 'Do you want to restore this item to its original location?',
		'msgbox_restore_all': 'Restore all items?',
		'msgbox_restore_all_desc': 'Do you want to restore all the items in here to their original location?',
		'msgbox_delete': 'Delete this item?',
		'msgbox_delete_desc': 'Are you sure you want to permanently delete this item?\nTHIS CANNOT BE UNDONE!',
		'msgbox_delete_all': 'Empty the Recycle Bin?',
		'msgbox_delete_all_desc': 'Are you sure you want to wipe out all your deleted items?\nThink twice before doing this, because you might not be able to recover them in the future...',

		'oglocation': 'Original location',
		'type': 'Type',
		'size': 'Size',
		'deldate': 'Deletion time',
		'rbin_in': 'Recycle Bin in',
		'discard': 'Discard',
		'preview': 'Preview',
		'help': 'Help',

		'back': 'Back',

		'ftype_desc_folder': 'File folder',
		'ftype_desc_txt': 'Text Document',
		'ftype_desc_ps1': 'Windows PowerShell Script',
		'ftype_desc_file_right': True,
		'ftype_desc_file': 'File',

		'main_loading': 'Loading Recycle Bin, please wait...',
		'main_warning': 'WARNING:',
		'main_rb_corrupt': 'The Recycle Bin on drive',
		'main_rb_corrupt_2': 'is corrupted.',
		'main_rbin_empty': 'The Recycle Bin is empty!',
		'main_rbin_metadata_unsupported_version': 'Your Recycle Bin contains metadata files that RBEditor can\'t read at the moment.\nTherefore, if you see some files missing or even no files, you know why now!',
		'main_new_item': 'New item',
		'main_restore_all': 'Restore all items',
		'main_empty_rb': 'Empty Recycle Bin',
		'main_open': 'Open',
		'main_delete': 'Delete',
		'main_restore': 'Restore',
		'main_properties': 'Properties',

		'itemedit_properties': 'Item properties',
		'itemedit_advanced': 'Advanced info',
		'itemedit_reduced': 'Reduced info',
		'itemedit_ogname': 'Original name',
		'itemedit_real_size': 'Real size',
		'itemedit_size_disk': 'Size in Recycle Bin',
		'itemedit_metadata_size': 'Metadata file size',
		'itemedit_rbin_name_i': 'File name in Recycle Bin (metadata file)',
		'itemedit_rbin_name_r': 'File name in Recycle Bin (data file)',
		'itemedit_rbin_location': 'Location',
		'itemedit_location_asterisk': '* You cannot access this folder\'s real contents with the File Explorer',

		'new_item_folder': 'Folder',
		'new_item_ext': 'Extension',
		'new_item_date_format_match': '(must match date format)',
	},
	'vi_VN': {
		'title': 'PHẦN MỀM CHỈNH SỬA THÙNG RÁC - RBEditor',
		'title_dtformat': 'Định dạng ngày giờ',
		'dtformat': 'Định dạng ngày giờ',
		'dtformat_preview': 'Định dạng ngày và giờ của bạn trông như thế nào khi được sử dụng:',
		'dtformat_guide': '''\
Nguồn: https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes
(đã dịch sang tiếng Việt)

%a - Tên viết tắt ngày trong tuần của ngôn ngữ.
%A - Tên đầy đủ ngày trong tuần của ngôn ngữ.
%w - Ngày trong tuần dưới dạng số thập phân, trong đó 0 là Chủ nhật và 6 là Thứ bảy.

%d - Ngày trong tháng dưới dạng số thập phân có đệm số không.
%b - Tháng là tên viết tắt của ngôn ngữ.
%B - Tháng là tên đầy đủ của ngôn ngữ.
%m - Tháng dưới dạng số thập phân không đệm.
%y - Năm không có thế kỷ dưới dạng số thập phân có đệm số không.
%Y - Năm với thế kỷ dưới dạng số thập phân.

%H - Giờ (đồng hồ 24 giờ) dưới dạng số thập phân có đệm số không.
%I - Giờ (đồng hồ 12 giờ) dưới dạng số thập phân có đệm số không.
%p - Phiên bản AM (SA) và PM (CH) của ngôn ngữ.
%M - Phút dưới dạng số thập phân có đệm số không.
%S - Giây dưới dạng số thập phân.
%f - Phần triệu giây dưới dạng số thập phân, có đệm số không thành 6 chữ số.
%z - Độ lệch UTC ở dạng '±HHMM[SS[.ffffff]]'.
%Z - Tên múi giờ.

%j - Ngày trong năm dưới dạng số thập phân có đệm số không.
%U - Số tuần của năm (Chủ nhật là ngày đầu tiên của tuần) dưới dạng số thập phân có đệm số không. Tất cả các ngày trong năm mới trước Chủ nhật đầu tiên được coi là trong tuần 0.
%W - Số tuần của năm (thứ Hai là ngày đầu tiên của tuần) dưới dạng số thập phân có đệm số không. Tất cả các ngày trong năm mới trước thứ Hai đầu tiên được coi là trong tuần 0.

%c - Biểu thị ngày và giờ thích hợp của ngôn ngữ.
%x - Đại diện ngày thích hợp của ngôn ngữ.
%X - Biểu thị thời gian thích hợp của ngôn ngữ.

%G - Năm theo tiêu chuẩn ISO 8601 với thế kỷ đại diện cho năm chứa phần lớn tuần theo tiêu chuẩn ISO (%V).
%u - ISO 8601 ngày trong tuần dưới dạng số thập phân trong đó 1 là thứ Hai.
%V - ISO 8601 tuần dưới dạng số thập phân với Thứ Hai là ngày đầu tuần. Tuần 01 là tuần có ngày 04/01.

%% - Ký tự '%' theo nghĩa đen.

Nếu bạn đã sử dụng bản phân phối Linux, bạn sẽ quen thuộc với quy trình này.\
''',

		'bytes': 'byte',

		'menubar_file': 'Tệp',
		'menubar_file_exit': 'Thoát',
		'menubar_edit': 'Sửa',
		'menubar_edit_reload': 'Tải lại Thùng rác',
		'menubar_settings': 'Cài đặt',
		'menubar_settings_dtformat': 'Định dạng ngày giờ...',
		'menubar_settings_language': 'Ngôn ngữ',
		'menubar_settings_language_system': 'Ngôn ngữ hệ thống',
		'menubar_help_update': 'Kiểm tra cập nhật',
		'menubar_help_about': 'Về ',

		'msgbox_error': 'Lỗi',
		'msgbox_warning': 'Cảnh báo',
		'msgbox_no_formatting': 'Chuỗi kí tự này không có định dạng. Bạn có vẫn muốn tiếp tục không?',
		'msgbox_blank': 'Chuỗi kí tự này không được để trống!',
		'msgbox_discard': 'Bạn có chắc chắn muốn hủy các thay đổi của mình không?',
		'msgbox_error_incorrect_fnamelen': 'Độ dài tên tệp không chính xác trong tệp',
		'msgbox_error_unsupported_version': 'Phiên bản tệp siêu dữ liệu không xác định hoặc không được hỗ trợ',
		'msgbox_n_a': 'Chưa được triển khai',
		'msgbox_n_a_desc': 'Tính năng này chưa được triển khai trong ',
		'msgbox_n_a_desc2': 'Xin lỗi',
		'msgbox_setting_change': 'Phần mềm bây giờ sẽ khởi động lại.\nMọi thay đổi chưa được lưu sẽ bị mất.',
		'msgbox_not_in_rb': 'Mục này không còn trong Thùng rác.\nMục này sẽ bị xóa khỏi danh sách này.',
		'msgbox_folder_warn': 'Khi mở một thư mục trong Thùng rác, bạn không thể mở bất kỳ thư mục con nào cho đến khi thư mục đó được khôi phục.\n\nBạn có muốn tiếp tục không?',
		'msgbox_lnk_warn': '''\
Tệp bạn vừa mở là tệp lối tắt (.lnk).

Nếu tệp hoặc thư mục mà tệp lối tắt này liên kết đến không còn tồn tại, Windows sẽ hiển thị lời nhắc hỏi bạn có muốn xóa tệp lối tắt hay không.
Nếu bạn chọn Có, lối tắt sẽ bị XÓA VĨNH VIỄN khỏi Thùng rác.

Nếu bạn đã vô tình mở tệp lối tắt này, không cần phải lo lắng, chỉ cần nhấn Không.

Bạn có muốn tiếp tục không?\
''',
		'msgbox_restore': 'Khôi phục khoản mục này?',
		'msgbox_restore_desc': 'Bạn có muốn khôi phục mục này về vị trí ban đầu không?',
		'msgbox_restore_all': 'Khôi phục tất cả khoản mục?',
		'msgbox_restore_all_desc': 'Bạn có muốn khôi phục tất cả khoản mục ở đây về vị trí ban đầu không?',
		'msgbox_delete': 'Xóa khoản mục này?',
		'msgbox_delete_desc': 'Bạn có chắc chắn muốn xóa vĩnh viễn mục này không?\nBẠN KHÔNG THỂ HOÀN TÁC THAO TÁC NÀY!',
		'msgbox_delete_all': 'Làm rỗng Thùng rác?',
		'msgbox_delete_all_desc': 'Bạn có chắc chắn muốn xóa tất cả các khoản mục đã xóa của mình không?\nHãy suy nghĩ kỹ trước khi thực hiện việc này, vì bạn đâu chắc là có thể khôi phục được chúng trong tương lai đâu...',

		'oglocation': 'Vị trí gốc',
		'type': 'Loại',
		'size': 'Kích cỡ',
		'deldate': 'Thời gian xóa',
		'rbin_in': 'Thùng rác ở',
		'discard': 'Huỷ bỏ',
		'preview': 'Xem trước',
		'help': 'Trợ giúp',

		'back': 'Quay lại',

		'ftype_desc_folder': 'Thư mục tệp',
		'ftype_desc_txt': 'Tài liệu văn bản',
		'ftype_desc_ps1': 'Tập lệnh Windows PowerShell',
		'ftype_desc_file_right': False,
		'ftype_desc_file': 'Tệp',

		'main_loading': 'Đang tải Thùng rác, vui lòng đợi...',
		'main_warning': 'CẢNH BÁO:',
		'main_rb_corrupt': 'Thùng rác trên ổ đĩa',
		'main_rb_corrupt_2': 'bị hỏng.',
		'main_rbin_empty': 'Thùng rác đang trống!',
		'main_rbin_metadata_unsupported_version': 'Thùng rác của bạn chứa các tệp siêu dữ liệu mà RBEditor hiện không thể đọc được.\nDo đó, nếu bạn thấy một số tệp bị thiếu hoặc thậm chí không có tệp nào, bạn đa biết tại sao rồi đó.',
		'main_new_item': 'Tạo khoản mục mới',
		'main_restore_all': 'Khôi phục mọi khoản mục',
		'main_empty_rb': 'Làm rỗng Thùng rác',
		'main_open': 'Mở',
		'main_delete': 'Xóa bỏ',
		'main_restore': 'Khôi phục',
		'main_properties': 'Thuộc tính',

		'itemedit_properties': 'Thuộc tính khoản mục',
		'itemedit_advanced': 'Thông tin chuyên sâu',
		'itemedit_reduced': 'Thông tin rút ngắn',
		'itemedit_ogname': 'Tên gốc',
		'itemedit_real_size': 'Kích cỡ chính xác',
		'itemedit_size_disk': 'Kích cỡ trong Thùng rác',
		'itemedit_metadata_size': 'Kích cỡ tệp siêu dữ liệu',
		'itemedit_rbin_name_i': 'Tên trong Thùng rác (tệp siêu dữ liệu)',
		'itemedit_rbin_name_r': 'Tên trong Thùng rác (tệp dữ liệu)',
		'itemedit_rbin_location': 'Vị trí',
		'itemedit_location_asterisk': '* Bạn không thể truy cập nội dung thực của thư mục này bằng File Explorer',

		'new_item_folder': 'Thư mục',
		'new_item_ext': 'Phần mở rộng',
		'new_item_date_format_match': '(phải khớp với định dạng ngày tháng)',
	}
}