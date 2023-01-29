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
Source: https://docs.python.org/3.6/library/datetime.html#strftime-and-strptime-behavior

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

		'about_running_on': 'Running on ',
		'about_running_on_right': False,
		'about_project_page': 'Project page: ',
		'about_beta_build': '\nWARNING: This is a pre-release version, therefore it may have bugs and/or glitches.\n',
		'about_licensed': 'Licensed under the ',
		'about_licensed2': ' license',
		'about_licensed_right': True,

		'bytes': 'bytes',

		'menubar_rbin': 'RBEditor',
		'menubar_rbin_reload': 'Reload Recycle Bin',
		'menubar_rbin_exit': 'Exit',
		'menubar_settings': 'Settings',
		'menubar_settings_dtformat': 'Date and time formatting...',
		'menubar_settings_language': 'Language',
		'menubar_settings_language_system': 'System Language',
		'menubar_settings_updates': 'Updates',
		'menubar_settings_updates_auto': 'Check for updates on startup',
		'menubar_settings_updates_prerelease': 'Check for pre-release versions',
		'menubar_help_update': 'Check for updates',
		'menubar_help_about': 'About ',
		'menubar_help_about_right': False,

		'msgbox_error': 'Error',
		'msgbox_warning': 'Warning',
		'msgbox_notice': 'Notice',
		'msgbox_no_formatting': 'This string has no formatting. Continue anyway?',
		'msgbox_blank': 'This string cannot be blank!',
		'msgbox_discard': 'Are you sure you want to discard your changes?',
		'msgbox_discard_item': 'Are you sure you want to discard this item?',
		'msgbox_overwrite1': 'The file ',
		'msgbox_overwrite2': ' already exists in its original location. Do you want to overwrite it?',
		'msgbox_error_incorrect_fnamelen': ': Incorrect file name length',
		'msgbox_error_unsupported_version': ': Unknown or unsupported metadata file version',
		'msgbox_error_unsupported_version_friendly': 'Invalid metadata file version!',
		'msgbox_error_invalid_metadata': ': Invalid metadata file',
		'msgbox_unicode_error': 'This text contains invalid Unicode characters.',
		'msgbox_size_int_error': 'Size must be an integer!',
		'msgbox_rbin_name_change': 'Do you want to update the Recycle Bin file name\'s extension with the new one you set?\nIf you leave it as-is, you might see "issues" when opening it.',
		'msgbox_n_a': 'Not implemented',
		'msgbox_n_a_desc': 'This feature is not implemented into this version of ',
		'msgbox_n_a_desc2': '. Sorry!',
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

		'msgbox_updater_exceeded': 'GitHub API rate limit exceeded! Please try again later.',
		'msgbox_updater_offline': 'Unable to connect to the internet. Please try again when you have a stable internet connection.',
		'msgbox_updater_unknown_error': 'Unable to check for updates! Please try again later.',
		'msgbox_updater_newupdate_title': 'Update available',
		'msgbox_updater_newupdate': 'An update is available!',
		'msgbox_updater_currver': 'Current version:',
		'msgbox_updater_newver': 'New version:',
		'msgbox_updater_prerelease': ' (pre-release)',
		'msgbox_updater_prompt': 'Do you want to go to the download page?',
		'msgbox_updater_latest': 'You are already using the latest version.',

		'oglocation': 'Original location',
		'type': 'Type',
		'size': 'Size',
		'deldate': 'Deletion time',
		'rbin_in': 'Recycle Bin in ',
		'rbin_in_right': False,
		'discard': 'Discard',
		'preview': 'Preview',
		'help': 'Help',
		'edit': 'Edit',

		'back': 'Back',

		'ftype_desc_folder': 'File folder',
		'ftype_desc_txt': 'Text Document',
		'ftype_desc_ini': 'Configuration settings',
		'ftype_desc_ps1': 'Windows PowerShell Script',
		'ftype_desc_ico': 'Icon',
		'ftype_desc_file_right': True,
		'ftype_desc_file': 'File',

		'main_loading': 'Loading Recycle Bin, please wait...',
		'main_updater': 'Checking for updates...',
		'main_warning': 'WARNING:',
		'main_rb_corrupt': 'The Recycle Bin on drive',
		'main_rb_corrupt_2': 'is corrupted.',
		'main_rbin_empty': 'The Recycle Bin is empty!',
		'main_rbin_metadata_unsupported_version': 'NOTE: Your Recycle Bin contained metadata files that RBEditor can\'t read.',
		'main_new_item': 'New item',
		'main_restore_all': 'Restore all items',
		'main_empty_rb': 'Empty Recycle Bin',
		'main_open': 'Open',
		'main_delete': 'Delete',
		'main_restore': 'Restore',
		'main_properties': 'Properties',
		'main_folder': '<folder>',

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
		'itemedit_version': 'Metadata file version',
		'itemedit_version_text': 'Version ',
		'itemedit_version_1': '(Windows Vista, 7, 8, 8.1)',
		'itemedit_version_2': '(Windows 10, 11)',
		'itemedit_version_text_unknown': '(Unknown)',
		'itemedit_location_asterisk': '* You cannot access this folder\'s real contents with the File Explorer',

		'new_item_edit': 'Edit existing item',
		'new_item_folder': 'Folder?',
		'new_item_bytes_note': '(in bytes)',
		'new_item_ext': 'Extension',
		'new_item_name': 'New Recycle Bin item',
		'new_item_version_warning': 'This metadata file version cannot be read by this version of Windows. Continue anyway?',
	},
	'vi_VN': {
		'title': 'PHẦN MỀM CHỈNH SỬA THÙNG RÁC - RBEditor',
		'title_dtformat': 'Định dạng ngày giờ',
		'dtformat': 'Định dạng ngày giờ',
		'dtformat_preview': 'Định dạng ngày và giờ của bạn trông như thế nào khi được sử dụng:',
		'dtformat_guide': '''\
Nguồn: https://docs.python.org/3.6/library/datetime.html#strftime-and-strptime-behavior
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

		'about_running_on': 'Đang chạy trên ',
		'about_running_on_right': False,
		'about_project_page': 'Trang dự án: ',
		'about_beta_build': '\nCẢNH BÁO: Đây là bản phát hành trước, do đó nó có thể có lỗi và/hoặc trục trặc.\n',
		'about_licensed': 'Được cấp phép theo giấy phép ',
		'about_licensed_right': False,

		'bytes': 'byte',

		'menubar_rbin': 'RBEditor',
		'menubar_rbin_reload': 'Tải lại Thùng rác',
		'menubar_rbin_exit': 'Thoát',
		'menubar_settings': 'Cài đặt',
		'menubar_settings_dtformat': 'Định dạng ngày giờ...',
		'menubar_settings_language': 'Ngôn ngữ',
		'menubar_settings_language_system': 'Ngôn ngữ hệ thống',
		'menubar_settings_updates': 'Cập nhật',
		'menubar_settings_updates_auto': 'Kiểm tra cập nhật khi khởi động',
		'menubar_settings_updates_prerelease': 'Kiểm tra phiên bản phát hành trước',
		'menubar_help_update': 'Kiểm tra cập nhật',
		'menubar_help_about': 'Về ',
		'menubar_help_about_right': False,

		'msgbox_error': 'Lỗi',
		'msgbox_warning': 'Cảnh báo',
		'msgbox_notice': 'Thông báo',
		'msgbox_no_formatting': 'Chuỗi kí tự này không có định dạng. Bạn có vẫn muốn tiếp tục không?',
		'msgbox_blank': 'Chuỗi kí tự này không được để trống!',
		'msgbox_discard': 'Bạn có chắc chắn muốn hủy các thay đổi của mình không?',
		'msgbox_discard_item': 'Bạn có chắc chắn muốn hủy khoản mục này không?',
		'msgbox_overwrite1': 'Tệp ',
		'msgbox_overwrite2': ' tồn tại ở vị trí ban đầu. Bạn có muốn thay thế tệp ở nơi nhận với tệp trong Thùng rác không?',
		'msgbox_error_incorrect_fnamelen': ': Độ dài tên tệp không chính xác',
		'msgbox_error_invalid_metadata': ': Tệp siêu dữ liệu không hợp lệ',
		'msgbox_error_unsupported_version': ': Phiên bản tệp siêu dữ liệu không xác định hoặc không được hỗ trợ',
		'msgbox_error_unsupported_version_friendly': 'Phiên bản tệp siêu dữ liệu không hợp lệ!',
		'msgbox_unicode_error': 'Chuỗi kí tự này chứa kí tự Unicode không hợp lệ.',
		'msgbox_size_int_error': 'Kích thước phải là một số nguyên!',
		'msgbox_rbin_name_change': 'Bạn có muốn cập nhật phần mở rộng của tên tệp Thùng rác bằng phần mở rộng mới mà bạn đã đặt không?\nNếu bạn để nó nguyên trạng, bạn có thể thấy "sự cố" khi mở nó.',
		'msgbox_n_a': 'Chưa được triển khai',
		'msgbox_n_a_desc': 'Tính năng này không được triển khai trong phiên bản này của ',
		'msgbox_n_a_desc2': '. Xin lỗi!',
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

		'msgbox_updater_exceeded': 'Đã vượt quá giới hạn tốc độ API GitHub! Vui lòng thử lại sau.',
		'msgbox_updater_offline': 'Không thể kết nối internet. Vui lòng thử lại khi bạn có đường truyền internet ổn định.',
		'msgbox_updater_unknown_error': 'Không thể kiểm tra cập nhật! Vui lòng thử lại sau.',
		'msgbox_updater_newupdate_title': 'Đã có bản cập nhật',
		'msgbox_updater_newupdate': 'Đã có bản cập nhật!',
		'msgbox_updater_currver': 'Phiên bản hiện tại:',
		'msgbox_updater_newver': 'Phiên bản mới:',
		'msgbox_updater_prerelease': ' (bản phát hành trước)',
		'msgbox_updater_prompt': 'Bạn có muốn truy cập trang tải xuống không?',
		'msgbox_updater_latest': 'Bạn đang sử dụng phiên bản mới nhất.',

		'oglocation': 'Vị trí gốc',
		'type': 'Loại',
		'size': 'Kích cỡ',
		'deldate': 'Thời gian xóa',
		'rbin_in': 'Thùng rác ở ',
		'rbin_in_right': False,
		'discard': 'Huỷ bỏ',
		'preview': 'Xem trước',
		'help': 'Trợ giúp',
		'edit': 'Chỉnh sửa',

		'back': 'Quay lại',

		'ftype_desc_folder': 'Thư mục tệp',
		'ftype_desc_txt': 'Tài liệu văn bản',
		'ftype_desc_ini': 'Cài đặt cấu hình',
		'ftype_desc_ps1': 'Tập lệnh Windows PowerShell',
		'ftype_desc_ico': 'Biếu tượng',
		'ftype_desc_file_right': False,
		'ftype_desc_file': 'Tệp',

		'main_loading': 'Đang tải Thùng rác, vui lòng đợi...',
		'main_updater': 'Đang kiểm tra cập nhật...',
		'main_warning': 'CẢNH BÁO:',
		'main_rb_corrupt': 'Thùng rác trên ổ đĩa',
		'main_rb_corrupt_2': 'bị hỏng.',
		'main_rbin_empty': 'Thùng rác đang trống!',
		'main_rbin_metadata_unsupported_version': 'LƯU Ý: Thùng rác của bạn đã chứa các tệp siêu dữ liệu mà RBEditor không thể đọc được.',
		'main_new_item': 'Tạo khoản mục mới',
		'main_restore_all': 'Khôi phục mọi khoản mục',
		'main_empty_rb': 'Làm rỗng Thùng rác',
		'main_open': 'Mở',
		'main_delete': 'Xóa bỏ',
		'main_restore': 'Khôi phục',
		'main_properties': 'Thuộc tính',
		'main_folder': '<thư mục>',

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
		'itemedit_version': 'Phiên bản tệp siêu dữ liệu',
		'itemedit_version_text': 'Phiên bản ',
		'itemedit_version_1': '(Windows Vista, 7, 8, 8.1)',
		'itemedit_version_2': '(Windows 10, 11)',
		'itemedit_version_text_unknown': '(Không xác định)',
		'itemedit_location_asterisk': '* Bạn không thể truy cập nội dung thực của thư mục này bằng File Explorer',

		'new_item_edit': 'Chỉnh sửa khoản mục',
		'new_item_folder': 'Thư mục?',
		'new_item_bytes_note': '(tính bằng byte)',
		'new_item_ext': 'Phần mở rộng',
		'new_item_name': 'Khoản mục Thùng rác mới',
		'new_item_version_warning': 'Phiên bản tệp siêu dữ liệu này không thể đọc được bằng phiên bản Windows này. Bạn có vẫn muốn tiếp tục không?',
	},
	'ja_JP': {
		'title': 'ごみ箱エディタ - RBEditor',
		'title_dtformat': '日付と時刻の形式',
		'dtformat': '日付と時刻の形式',
		'dtformat_preview': '日付と時刻の形式を使用した場合の外観：',
		'dtformat_guide': '''\
ソース： https://docs.python.org/ja/3.6/library/datetime.html#strftime-and-strptime-behavior

%a - ロケールの曜日名を短縮形で表示します。
%A - ロケールの曜日名を表示します。
%w - 曜日を10進表記した文字列を表示します。0 が日曜日で、6 が土曜日を表します。

%d - 0埋めした10進数で表記した月中の日にち。
%b - ロケールの月名を短縮形で表示します。
%B - ロケールの月名を表示します。
%m - 0埋めした10進数で表記した月。
%y - 0埋めした10進数で表記した世紀無しの年。
%Y - 西暦（4桁）の 10 進表記を表します。

%H - 0埋めした10進数で表記した時（24時間表記）。
%I - 0埋めした10進数で表記した時（12時間表記）。
%p - ロケールの AM もしくは PM と等価な文字列になります。
%M - 0埋めした10進数で表記した分。
%S - 0埋めした10進数で表記した秒。
%f - 10進数で表記したマイクロ秒 (左側から0埋めされます)。
%z - UTCオフセットを ±HHMM[SS[.ffffff]] の形式で表示します。
%Z - タイムゾーンの名前を表示します。

%j - 0埋めした10進数で表記した年中の日にち。
%U - 0埋めした10進数で表記した年中の週番号 (週の始まりは日曜日とする)。新年の最初の日曜日に先立つ日は 0週に属するとします。
%W - 0埋めした10進数で表記した年中の週番号 (週の始まりは月曜日とする)。新年の最初の月曜日に先立つ日は 0週に属するとします。

%c - ロケールの日時を適切な形式で表します。
%x - ロケールの日付を適切な形式で表します。
%X - ロケールの時間を適切な形式で表します。

%G - ISO week(%V)の内過半数を含む西暦表記の ISO 8601 year です。
%u - 1 を月曜日を表す 10進数表記の ISO 8601 weekday です。
%V - 週で最初の月曜日を始めとする ISO 8601 week です。 Week 01 は 1月4日を含みます。

%% - 文字 '%' を表します。

Linux ディストリビューションを使用したことがある場合は、このプロセスに精通している必要があります。\
''',

		'about_running_on': 'での実行',
		'about_running_on_right': True,
		'about_project_page': 'プロジェクトページ：',
		'about_beta_build': '\n警告：これはプレリリース バージョンであるため、バグやグリッチがある可能性があります。\n',
		'about_licensed': '',
		'about_licensed2': 'ライセンスの下でライセンスされています',
		'about_licensed_right': True,

		'bytes': 'バイト',

		'menubar_rbin': 'RBEditor',
		'menubar_rbin_reload': 'ごみ箱をリロードする',
		'menubar_rbin_exit': '出口',
		'menubar_settings': '設定',
		'menubar_settings_dtformat': '日付と時刻の形式...',
		'menubar_settings_language': '言語',
		'menubar_settings_language_system': 'システム言語',
		'menubar_settings_updates': '更新',
		'menubar_settings_updates_auto': '起動時に更新を確認する',
		'menubar_settings_updates_prerelease': 'プレリリース バージョンを確認する',
		'menubar_help_update': '更新を確認する',
		'menubar_help_about': ' について',
		'menubar_help_about_right': True,

		'msgbox_error': 'エラー',
		'msgbox_warning': '警告',
		'msgbox_notice': '知らせ',
		'msgbox_no_formatting': 'この文字列にはフォーマットがありません。 とにかく続けます？',
		'msgbox_blank': 'この文字列を空白にすることはできません!',
		'msgbox_discard': '変更を破棄してもよろしいですか?',
		'msgbox_discard_item': '本当にこの項目を破棄しますか?',
		'msgbox_overwrite1': 'ファイル',
		'msgbox_overwrite2': 'は、元の場所に既に存在します。 上書きしますか？',
		'msgbox_error_incorrect_fnamelen': '：ファイル名の長さが正しくありません',
		'msgbox_error_unsupported_version': '：メタデータ ファイルのバージョンが不明またはサポートされていません',
		'msgbox_error_unsupported_version_friendly': '無効なメタデータ ファイルのバージョンです！',
		'msgbox_error_invalid_metadata': '：メタデータ ファイルが無効です',
		'msgbox_error_invalid_date': '：無効な削除日',
		'msgbox_unicode_error': 'このテキストには無効な Unicode 文字が含まれています。',
		'msgbox_size_int_error': 'サイズは整数でなければなりません！',
		'msgbox_rbin_name_change': 'ごみ箱のファイル名の拡張子を、設定した新しい拡張子に更新しますか？\nそのままにしておくと、開いたときに「問題」が発生する可能性があります。',
		'msgbox_n_a': '未実装',
		'msgbox_n_a_desc': 'この機能は、このバージョンの ',
		'msgbox_n_a_desc2': ' には実装されていません。 ごめん！',
		'msgbox_setting_change': 'プログラムが再起動します。\n保存されていない変更は失われます。',
		'msgbox_not_in_rb': 'このアイテムはごみ箱にありません。\nこのリストから削除されます。',
		'msgbox_folder_warn': 'ごみ箱のフォルダを開く場合、フォルダが復元されるまでサブフォルダを開くことはできません。\n\n続行しますか?',
		'msgbox_lnk_warn': '''\
開いたファイルはショートカット ファイル (.lnk) でした。

このショートカットがリンクしているファイルまたはフォルダーが存在しない場合、Windows はショートカットを削除するかどうかを尋ねるプロンプトを表示します。
[はい] を選択すると、ショートカットはごみ箱から完全に削除されます。

誤ってショートカットを開いてしまった場合でも、心配する必要はありません。[いいえ] を押してください。

続けたいですか？\
''',
		'msgbox_restore': 'このアイテムを復元しますか？',
		'msgbox_restore_desc': 'このアイテムを元の場所に復元しますか?',
		'msgbox_restore_all': 'すべての項目を復元しますか?',
		'msgbox_restore_all_desc': 'ここにあるすべての項目を元の場所に復元しますか?',
		'msgbox_delete': 'この項目を削除しますか?',
		'msgbox_delete_desc': 'この項目を完全に削除してもよろしいですか?\nこれは、元に戻すことはできません！',
		'msgbox_delete_all': 'ごみ箱を空にする？',
		'msgbox_delete_all_desc': '削除済みアイテムをすべて消去してもよろしいですか?\n将来復元できない可能性があるため、これを行う前によく考えてください...',

		'msgbox_updater_exceeded': 'GitHub API のレート制限を超えました! 後でもう一度やり直してください。',
		'msgbox_updater_offline': 'インターネットに接続できません。 インターネット接続が安定しているときにもう一度お試しください。',
		'msgbox_updater_unknown_error': 'アップデートを確認できません！ 後でもう一度やり直してください。',
		'msgbox_updater_newupdate_title': '利用可能なアップデート',
		'msgbox_updater_newupdate': 'アップデートが利用可能です！',
		'msgbox_updater_currver': '現行版：',
		'msgbox_updater_newver': '新しいバージョン：',
		'msgbox_updater_prerelease': '（プレリリース）',
		'msgbox_updater_prompt': 'ダウンロードページに行きますか？',
		'msgbox_updater_latest': 'すでに最新バージョンを使用しています。',

		'oglocation': '元の場所',
		'type': '種類',
		'size': 'サイズ',
		'deldate': '削除時間',
		'rbin_in': 'のごみ箱',
		'rbin_in_right': True,
		'discard': '破棄',
		'preview': 'プレビュー',
		'help': 'ヘルプ',
		'edit': '編集',

		'back': '戻る',

		'ftype_desc_folder': 'ファイル フォルダー',
		'ftype_desc_txt': 'テキスト ドキュメント',
		'ftype_desc_ini': '構成設定',
		'ftype_desc_ps1': 'Windows PowerShell スクリプト',
		'ftype_desc_ico': 'アイコン',
		'ftype_desc_file_right': True,
		'ftype_desc_file': 'ファイル',

		'main_loading': 'ごみ箱を読み込んでいます。お待ちください...',
		'main_updater': 'アップデートの確認...',
		'main_warning': '警告：',
		'main_rb_corrupt': 'ドライブ',
		'main_rb_corrupt_2': 'のごみ箱が破損しています。',
		'main_rbin_empty': 'ごみ箱が空です！',
		'main_rbin_metadata_unsupported_version': '知らせ：ごみ箱には、RBEditor が読み取れないメタデータ ファイルが含まれていました。',
		'main_new_item': '新しい項目',
		'main_restore_all': 'すべての項目を復元する',
		'main_empty_rb': 'ごみ箱を空にする',
		'main_open': '開く',
		'main_delete': '削除',
		'main_restore': '戻す',
		'main_properties': 'プロパティ',
		'main_folder': '< フォルダー >',

		'itemedit_properties': '項目のプロパティ',
		'itemedit_advanced': 'アドバンス情報',
		'itemedit_reduced': '縮小情報',
		'itemedit_ogname': '元の名前',
		'itemedit_real_size': 'リアルサイズ',
		'itemedit_size_disk': 'ごみ箱のサイズ',
		'itemedit_metadata_size': 'メタデータ ファイルのサイズ',
		'itemedit_rbin_name_i': 'ごみ箱のファイル名（メタデータファイル）',
		'itemedit_rbin_name_r': 'ごみ箱のファイル名（データファイル）',
		'itemedit_rbin_location': '場所',
		'itemedit_version': 'メタデータ ファイルのバージョン',
		'itemedit_version_text': 'バージョン',
		'itemedit_version_1': '（Windows Vista、7、8、8.1）',
		'itemedit_version_2': '（Windows 10、11）',
		'itemedit_version_text_unknown': '（わからない）',
		'itemedit_location_asterisk': '* ファイル エクスプローラーでこのフォルダーの実際の内容にアクセスすることはできません',

		'new_item_edit': '既存の項目を編集',
		'new_item_folder': 'フォルダ？',
		'new_item_bytes_note': '（バイト単位）',
		'new_item_ext': '拡大',
		'new_item_name': '新しいごみ箱項目',
		'new_item_version_warning': 'このメタデータ ファイルのバージョンは、このバージョンの Windows では読み取ることができません。 それでも続行しますか？',
	},
}