import sys
if __name__ == '__main__':
	print('Please run main.py to start the program!')
	sys.exit()

lang = {
	'en': {
		'info': '''\
English - original language of RBEditor
(c) 2022-2023 GamingWithEvets Inc.\
''',

		'qmark': '?',

		'title': 'RECYCLE BIN EDITOR - RBEditor',
		'title_dtformat': 'Date and time formatting',
		'dtformat': 'Date and time format',
		'dtformat_preview': 'What your date and time format looks like when used:',
		'dtformat_guide': '''\
Source: https://docs.python.org/3.6/library/datetime.html#strftime-and-strptime-behavior

%a - Weekday as locale's abbreviated name.
%A - Weekday as locale's full name.
%w - Weekday as a decimal number, where 0 is Sunday and 6 is Saturday.

%d - Day of the month as a zero-padded decimal number.
%b - Month as locale's abbreviated name.
%B - Month as locale's full name.
%m - Month as a zero-padded decimal number.
%y - Year without century as a zero-padded decimal number.
%Y - Year with century as a decimal number.

%H - Hour (24-hour clock) as a zero-padded decimal number.
%I - Hour (12-hour clock) as a zero-padded decimal number.
%p - Locale's equivalent of either AM or PM.
%M - Minute as a zero-padded decimal number.
%S - Second as a zero-padded decimal number.
%f - Microsecond as a decimal number, zero-padded to 6 digits.
%z - UTC offset in the form '±HHMM[SS[.ffffff]]'.
%Z - Time zone name.

%j - Day of the year as a zero-padded decimal number.
%U - Week number of the year (Sunday as the first day of the week) as a zero-padded decimal number. All days in a new year preceding the first Sunday are considered to be in week 0.
%W - Week number of the year (Monday as the first day of the week) as a zero-padded decimal number. All days in a new year preceding the first Monday are considered to be in week 0.

%c - Locale's appropriate date and time representation.
%x - Locale's appropriate date representation.
%X - Locale's appropriate time representation.

%G - ISO 8601 year with century representing the year that contains the greater part of the ISO week (%V).
%u - ISO 8601 weekday as a decimal number where 1 is Monday.
%V - ISO 8601 week as a decimal number with Monday as the first day of the week. Week 01 is the week containing Jan 4.

%% - A literal '%' character.

If you have used a Linux distribution you should be familiar with this process.\
''',

		'about_running_on': 'Running on {}',
		'about_project_page': 'Project page: ',
		'about_beta_build': '\nWARNING: This is a pre-release version, therefore it may have bugs and/or glitches.\n',
		'about_licensed': 'Licensed under the {} license',

		'bytes': 'bytes',
		'KB': 'KB',
		'KiB': 'KiB',
		'MB': 'MB',
		'MiB': 'MiB',
		'GB': 'GB',
		'GiB': 'GiB',
		'TB': 'TB',
		'TiB': 'TiB',
		'PB': 'PB',
		'PiB': 'PiB',
		'EB': 'EB',
		'EiB': 'EiB',
		'ZB': 'ZB',
		'ZiB': 'ZiB',
		'YB': 'YB',
		'YiB': 'YiB',

		'menubar_rbin_sid': 'Your SID: ',
		'menubar_rbin_reload': 'Reload Recycle Bin',
		'menubar_rbin_explorer_bin': 'Open Recycle Bin in File Explorer',
		'menubar_rbin_exit': 'Exit',
		'menubar_settings': 'Settings',
		'menubar_settings_rbin_view': 'Recycle Bin view',
		'menubar_settings_rbin_view_felike': 'File Explorer-like',
		'menubar_settings_rbin_view_legacy': 'Legacy view',
		'menubar_settings_sort_method': 'File sorting',
		'menubar_settings_sort_method_natsort': 'Natural sorting',
		'menubar_settings_sort_method_lexico': 'Lexicographical sorting',
		'menubar_settings_sort_method_folders_first': 'Show folders first',
		'menubar_settings_dtformat': 'Date and time formatting...',
		'menubar_settings_language': 'Language',
		'menubar_settings_language_system': 'System language',
		'menubar_settings_language_info': 'Info for current language',
		'menubar_settings_locale': 'Locale',
		'menubar_settings_locale_lang': 'Language locale',
		'menubar_settings_locale_system': 'System locale',
		'menubar_settings_locale_custom': 'Custom',
		'menubar_settings_locale_custom2': ' ({})',
		'menubar_settings_updates': 'Updates',
		'menubar_settings_updates_auto': 'Check for updates on startup',
		'menubar_settings_updates_prerelease': 'Check for pre-release versions',
		'menubar_help_update': 'Check for updates',
		'menubar_help_about': 'About {}',

		'msgbox_error': 'Error',
		'msgbox_warning': 'Warning',
		'msgbox_notice': 'Notice',
		'msgbox_no_formatting': 'This string has no formatting. Continue anyway?',
		'msgbox_blank': 'This string cannot be blank!',
		'msgbox_discard': 'Are you sure you want to discard your changes?',
		'msgbox_discard_item': 'Are you sure you want to discard this item?',
		'msgbox_overwrite': 'The file {} already exists in its original location. Do you want to overwrite it?',
		'msgbox_error_unsupported_version': ': Unknown or unsupported metadata file version',
		'msgbox_error_invalid_metadata': ': Invalid metadata file',
		'msgbox_error_unicode': 'This string contains Unicode characters not supported by this version of Tcl/Tk.',
		'msgbox_unsupported_tcl': 'It looks like you are running Python {}, which has a version of Tcl/Tk that doesn\'t support some Unicode characters.\n\nDo you want to continue?',
		'msgbox_rbin_name_change': 'Do you want to update the Recycle Bin file name\'s extension with the new one you set?\nIf you leave it as-is, you might see "issues" when opening it.',
		'msgbox_rbin_name_change_2': 'Changing the "Folder" property will require deletion of the item\'s old data.\nDo you want to continue with deletion? If you select No, the "Folder" property will not change.',
		'msgbox_n_a': 'Not implemented',
		'msgbox_n_a_desc': 'This feature is not implemented into this version of {}. Sorry!',
		'msgbox_reload_confirm': 'Are you sure you want to reload the Recycle Bin? You will return to the main menu.',
		'msgbox_reload_next_reboot': 'The changes will take effect the next time you open the program.',
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

		'ogname': 'Name',
		'oglocation': 'Original location',
		'type': 'Type',
		'size': 'Size',
		'deldate': 'Deletion time',
		'rbin_in': 'Recycle Bin in {}',
		'discard': 'Discard',
		'preview': 'Preview',
		'reset': 'Reset to defaults',
		'help': 'Help',
		'edit': 'Edit',

		'back': 'Back',
		'cancel': 'Cancel',

		'ftype_desc_folder': 'File folder',
		'ftype_desc_txt': 'Text Document',
		'ftype_desc_ini': 'Configuration settings',
		'ftype_desc_ps1': 'Windows PowerShell Script',
		'ftype_desc_ico': 'Icon',
		'ftype_desc_file': 'File',
		'ftype_desc_file_space': '{} File',

		'main_loading': 'Loading Recycle Bin, please wait...',
		'main_warning': 'WARNING:',
		'main_rb_corrupt': 'The Recycle Bin on drive {} is corrupted.',
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

		'itemproperties_properties': 'Item properties',
		'itemproperties_advanced': 'Advanced info',
		'itemproperties_reduced': 'Reduced info',
		'itemproperties_ogname': 'Original name',
		'itemproperties_ogname_unterminated': '(unterminated string)',
		'itemproperties_real_size': 'Real size',
		'itemproperties_size_disk': 'Size in Recycle Bin',
		'itemproperties_metadata_size': 'Metadata file size',
		'itemproperties_rbin_name_i': 'File name in Recycle Bin (metadata file)',
		'itemproperties_rbin_name_r': 'File name in Recycle Bin (data file)',
		'itemproperties_rbin_location': 'Location',
		'itemproperties_version': 'Metadata file version',
		'itemproperties_version_text': 'Version ',
		'itemproperties_location_asterisk': '* Relative paths start from the Desktop',
		'itemproperties_location_asterisk_2': '** You cannot access this folder\'s real contents with the File Explorer',

		'new_item_edit': 'Edit existing item',
		'new_item_path': 'Original file path',
		'new_item_folder': 'Folder?',
		'new_item_bytes_note': '(in bytes)',
		'new_item_ext': 'Extension',
		'new_item_name': 'New Recycle Bin item',
		'new_item_version_warning': 'This metadata file version cannot be read by this version of Windows. Continue anyway?',
		'new_item_size_int_error': 'Size must be an integer!',
		'new_item_size_out_of_range': 'Size must be between -(2^63) and 2^63-1',
		'new_item_error_unsupported_version': 'Invalid metadata file version!',
		'new_item_invalid_path': 'File path must not have the following characters:',
		'new_item_invalid_path_2': 'File path must include directories!',
		'new_item_invalid_path_3': 'Invalid file path!',
		'new_item_invalid_path_4': 'File path must be absolute!',

		'new_item_hacker_mode': 'Hacker mode',
		'new_item_hacker_mode_note': '(to bypass this error, enable hacker mode!)',
		'new_item_hacker_mode_enable': 'Enable hacker mode',
		'new_item_hacker_mode_no_terminator': 'Unterminated file path (metadata version 2 only)',

		'locale_chooser_title': 'Locale select',
		'locale_chooser_choose': 'Select a locale:',

		'dtpicker_title': 'Date and time picker',
		'dtpicker_type': 'Input type',
		'dtpicker_type_basic': 'Basic',
		'dtpicker_day': 'Day',
		'dtpicker_month': 'Month',
		'dtpicker_year': 'Year',
		'dtpicker_hour': 'Hours',
		'dtpicker_minute': 'Minutes',
		'dtpicker_second': 'Seconds',
		'dtpicker_microsecond': 'Microseconds',
		'dtpicker_ft_header': 'Time (FILETIME format)',
		'dtpicker_ft_learn_more': 'Learn more about FILETIME',
		'dtpicker_ft_int_error': 'FILETIME must be an integer!',
		'dtpicker_ft_out_of_range': 'FILETIME not in valid range!',

		'updater_title': 'Updater',
		'updater_checking': 'Checking for updates...',
		'updater_donotclose': 'DO NOT close the program\nwhile checking for updates',
		'updater_exceeded': 'GitHub API rate limit exceeded!\nPlease try again later.',
		'updater_offline': 'Unable to connect to the internet. Please try again\nwhen you have a stable internet connection.',
		'updater_unknown_error': 'Unable to check for updates!\nPlease try again later.',
		'updater_newupdate': 'An update is available!',
		'updater_currver': 'Current version: ',
		'updater_newver': 'New version: ',
		'updater_prerelease': ' (pre-release)',
		'updater_latest': 'You are already using the latest version.',
		'updater_download': 'Visit download page',
	},
	'vi': {
		'info': '''\
Tiếng Việt - ngôn ngữ thứ hai của RBEditor
(c) 2022-2023 GamingWithEvets Inc.\
''',

		'title': 'TRÌNH CHỈNH SỬA THÙNG RÁC - RBEditor',
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
%m - Tháng dưới dạng số thập phân có đệm số không.
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

		'about_running_on': 'Đang chạy trên {}',
		'about_project_page': 'Trang dự án: ',
		'about_beta_build': '\nCẢNH BÁO: Đây là bản phát hành trước, do đó nó có thể có lỗi và/hoặc trục trặc.\n',
		'about_licensed': 'Được cấp phép theo giấy phép {}',

		'bytes': 'byte',

		'menubar_rbin_sid': 'SID của bạn là: ',
		'menubar_rbin_reload': 'Tải lại Thùng rác',
		'menubar_rbin_explorer_bin': 'Mở Thùng rác trong File Explorer',
		'menubar_rbin_exit': 'Thoát',
		'menubar_settings': 'Cài đặt',
		'menubar_settings_rbin_view': 'Chế độ xem Thùng rác',
		'menubar_settings_rbin_view_felike': 'Giống File Explorer',
		'menubar_settings_rbin_view_legacy': 'Chế độ xem cũ',
		'menubar_settings_sort_method': 'Sắp xếp tệp',
		'menubar_settings_sort_method_natsort': 'Sắp xếp tự nhiên',
		'menubar_settings_sort_method_lexico': 'Sắp xếp theo thứ tự từ điển',
		'menubar_settings_sort_method_folders_first': 'Hiển thị thư mục trước',
		'menubar_settings_dtformat': 'Định dạng ngày giờ...',
		'menubar_settings_language': 'Ngôn ngữ',
		'menubar_settings_language_system': 'Ngôn ngữ hệ thống',
		'menubar_settings_language_info': 'Thông tin về ngôn ngữ hiện tại',
		'menubar_settings_locale_lang': 'Locale ngôn ngữ',
		'menubar_settings_locale_system': 'Locale hệ thống',
		'menubar_settings_locale_custom': 'Tùy chọn',
		'menubar_settings_updates': 'Cập nhật',
		'menubar_settings_updates_auto': 'Kiểm tra cập nhật khi khởi động',
		'menubar_settings_updates_prerelease': 'Kiểm tra phiên bản phát hành trước',
		'menubar_help_update': 'Kiểm tra cập nhật',
		'menubar_help_about': 'Về {}',

		'msgbox_error': 'Lỗi',
		'msgbox_warning': 'Cảnh báo',
		'msgbox_notice': 'Thông báo',
		'msgbox_no_formatting': 'Chuỗi kí tự này không có định dạng. Bạn có vẫn muốn tiếp tục không?',
		'msgbox_blank': 'Chuỗi kí tự này không được để trống!',
		'msgbox_discard': 'Bạn có chắc chắn muốn hủy các thay đổi của mình không?',
		'msgbox_discard_item': 'Bạn có chắc chắn muốn hủy khoản mục này không?',
		'msgbox_overwrite': 'Tệp {} tồn tại ở vị trí ban đầu. Bạn có muốn thay thế tệp ở nơi nhận với tệp trong Thùng rác không?',
		'msgbox_error_invalid_metadata': ': Tệp siêu dữ liệu không hợp lệ',
		'msgbox_error_unsupported_version': ': Phiên bản tệp siêu dữ liệu không xác định hoặc không được hỗ trợ',
		'msgbox_error_unicode': 'Chuỗi kí tự này chứa các ký tự Unicode không được hỗ trợ bởi phiên bản Tcl/Tk này.',
		'msgbox_unsupported_tcl': 'Có vẻ như bạn đang chạy Python {}, phiên bản này có phiên bản Tcl/Tk không hỗ trợ một số ký tự Unicode.\n\nBạn có muốn tiếp tục không?',
		'msgbox_rbin_name_change': 'Bạn có muốn cập nhật phần mở rộng của tên tệp Thùng rác bằng phần mở rộng mới mà bạn đã đặt không?\nNếu bạn để nó nguyên trạng, bạn có thể thấy "sự cố" khi mở nó.',
		'msgbox_rbin_name_change_2': 'Thay đổi thuộc tính "Thư mục" sẽ yêu cầu xóa tất cả dữ liệu cũ của khoản mục.\nBạn có muốn tiếp tục với quá trình xóa không? Nếu bạn chọn Không, thuộc tính "Thư mục" sẽ không thay đổi.',
		'msgbox_n_a': 'Chưa được triển khai',
		'msgbox_n_a_desc': 'Tính năng này không được triển khai trong phiên bản này của {}. Xin lỗi!',
		'msgbox_reload_confirm': 'Bạn có chắc chắn muốn tải lại Thùng rác không? Bạn sẽ được đưa về màn hình chính.',
		'msgbox_reload_next_reboot': 'Những thay đổi sẽ có hiệu lực vào lần mở tiếp theo.',
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

		'ogname': 'Tên',
		'oglocation': 'Vị trí gốc',
		'type': 'Loại',
		'size': 'Kích cỡ',
		'deldate': 'Thời gian xóa',
		'rbin_in': 'Thùng rác ở {}',
		'discard': 'Huỷ bỏ',
		'preview': 'Xem trước',
		'reset': 'Đặt lại về mặc định',
		'help': 'Trợ giúp',
		'edit': 'Chỉnh sửa',

		'back': 'Quay lại',
		'cancel': 'Huỷ bỏ',

		'ftype_desc_folder': 'Thư mục tệp',
		'ftype_desc_txt': 'Tài liệu văn bản',
		'ftype_desc_ini': 'Cài đặt cấu hình',
		'ftype_desc_ps1': 'Tập lệnh Windows PowerShell',
		'ftype_desc_ico': 'Biếu tượng',
		'ftype_desc_file': 'Tệp',
		'ftype_desc_file_space': 'Tệp {}',

		'main_loading': 'Đang tải Thùng rác, vui lòng đợi...',
		'main_warning': 'CẢNH BÁO:',
		'main_rb_corrupt': 'Thùng rác trên ổ đĩa {} bị hỏng.',
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

		'itemproperties_properties': 'Thuộc tính khoản mục',
		'itemproperties_advanced': 'Thông tin chuyên sâu',
		'itemproperties_reduced': 'Thông tin rút ngắn',
		'itemproperties_ogname': 'Tên gốc',
		'itemproperties_ogname_unterminated': '(không có kí tự kết thúc)',
		'itemproperties_real_size': 'Kích cỡ chính xác',
		'itemproperties_size_disk': 'Kích cỡ trong Thùng rác',
		'itemproperties_metadata_size': 'Kích cỡ tệp siêu dữ liệu',
		'itemproperties_rbin_name_i': 'Tên trong Thùng rác (tệp siêu dữ liệu)',
		'itemproperties_rbin_name_r': 'Tên trong Thùng rác (tệp dữ liệu)',
		'itemproperties_rbin_location': 'Vị trí',
		'itemproperties_version': 'Phiên bản tệp siêu dữ liệu',
		'itemproperties_version_text': 'Phiên bản ',
		'itemproperties_location_asterisk': '* Địa chỉ tương đối bắt đầu từ Bàn làm việc',
		'itemproperties_location_asterisk_2': '** Bạn không thể truy cập nội dung thực của thư mục này bằng File Explorer',

		'new_item_edit': 'Chỉnh sửa khoản mục',
		'new_item_path': 'Địa chỉ tệp gốc',
		'new_item_folder': 'Thư mục?',
		'new_item_bytes_note': '(tính bằng byte)',
		'new_item_ext': 'Phần mở rộng',
		'new_item_name': 'Khoản mục Thùng rác mới',
		'new_item_version_warning': 'Phiên bản tệp siêu dữ liệu này không thể đọc được bằng phiên bản Windows này. Bạn có vẫn muốn tiếp tục không?',
		'new_item_size_int_error': 'Kích thước phải là một số nguyên!',
		'new_item_size_out_of_range': 'Kích thước phải từ -(2^63) đến 2^63-1',
		'new_item_error_unsupported_version': 'Phiên bản tệp siêu dữ liệu không hợp lệ!',
		'new_item_invalid_path': 'Đường dẫn tập tin không được có các ký tự sau:',
		'new_item_invalid_path_2': 'Đường dẫn tệp phải bao gồm thư mục!',
		'new_item_invalid_path_3': 'Đường dẫn tệp không hợp lệ!',
		'new_item_invalid_path_4': 'Đường dẫn tệp phải là đường dẫn tuyệt đối!',

		'new_item_hacker_mode': 'Chế độ hacker',
		'new_item_hacker_mode_note': '(để tránh lỗi này, hãy bật chế độ hacker!)',
		'new_item_hacker_mode_enable': 'Bật chế độ hacker',
		'new_item_hacker_mode_no_terminator': 'Đường dẫn tệp không có kí tự kết thúc (chỉ cho tệp siêu dữ liệu phiên bản 2)',

		'locale_chooser_title': 'Chọn locale',
		'locale_chooser_choose': 'Chọn một locale:',

		'dtpicker_title': 'Bộ chọn ngày và giờ',
		'dtpicker_type': 'Kiểu nhập liệu',
		'dtpicker_type_basic': 'Cơ bản',
		'dtpicker_day': 'Ngày',
		'dtpicker_month': 'Tháng',
		'dtpicker_year': 'Năm',
		'dtpicker_hour': 'Giờ',
		'dtpicker_minute': 'Phút',
		'dtpicker_second': 'Giây',
		'dtpicker_microsecond': 'Micro giây',
		'dtpicker_ft_header': 'Thời gian (Định dạng FILETIME)',
		'dtpicker_ft_learn_more': 'Tìm hiểu thêm về FILETIME',
		'dtpicker_ft_int_error': 'FILETIME phải là một số nguyên!',
		'dtpicker_ft_out_of_range': 'FILETIME không nằm trong phạm vi hợp lệ!',

		'updater_title': 'Chương trình cập nhật',
		'updater_checking': 'Đang kiểm tra cập nhật...',
		'updater_donotclose': 'KHÔNG đóng chương trình\ntrong khi kiểm tra cập nhật',
		'updater_exceeded': 'Đã vượt quá giới hạn tốc độ API GitHub!\nVui lòng thử lại sau.',
		'updater_offline': 'Không thể kết nối internet. Vui lòng thử lại\nkhi bạn có đường truyền internet ổn định.',
		'updater_unknown_error': 'Không thể kiểm tra cập nhật!\nVui lòng thử lại sau.',
		'updater_newupdate': 'Đã có bản cập nhật!',
		'updater_currver': 'Phiên bản hiện tại: ',
		'updater_newver': 'Phiên bản mới: ',
		'updater_prerelease': ' (bản phát hành trước)',
		'updater_prompt': 'Bạn có muốn truy cập trang tải xuống không?',
		'updater_latest': 'Bạn đang sử dụng phiên bản mới nhất.',
		'updater_download': 'Truy cập trang tải xuống',
	},
	'ja': {
		'info': '''\
日本語 - RBEditor の第３言語
(c) 2023 GamingWithEvets Inc.\
''',

		'qmark': '？',

		'title': 'ごみ箱エディタ - RBEditor',
		'title_dtformat': '日付と時刻の形式',
		'dtformat': '日付と時刻の形式',
		'dtformat_preview': '日付と時刻の形式を使用した場合の外観：',
		'dtformat_guide': '''\
ソース： https://docs.python.org/ja/3.6/library/datetime.html#strftime-and-strptime-behavior

%a - ロケールの曜日名を短縮形で表示します。
%A - ロケールの曜日名を表示します。
%w - 曜日を10進表記した文字列を表示します。0が日曜日で、6が土曜日を表します。

%d - 0埋めした10進数で表記した月中の日にち。
%b - ロケールの月名を短縮形で表示します。
%B - ロケールの月名を表示します。
%m - 0埋めした10進数で表記した月。
%y - 0埋めした10進数で表記した世紀無しの年。
%Y - 西暦（4桁）の10進表記を表します。

%H - 0埋めした10進数で表記した時（24時間表記）。
%I - 0埋めした10進数で表記した時（24時間表記）。
%p - ロケールの AM もしくは PM と等価な文字列になります。
%M - 0埋めした10進数で表記した分。
%S - 0埋めした10進数で表記した秒。
%f - 10進数で表記したマイクロ秒（左側から0埋めされます）。
%z - UTCオフセットを ±HHMM[SS[.ffffff]] の形式で表示します。
%Z - タイムゾーンの名前を表示します。

%j - 0埋めした10進数で表記した年中の日にち。
%U - 0埋めした10進数で表記した年中の週番号（週の始まりは日曜日とする）。新年の最初の日曜日に先立つ日は0週に属するとします。
%W - 0埋めした10進数で表記した年中の週番号（週の始まりは月曜日とする）。新年の最初の月曜日に先立つ日は0週に属するとします。

%c - ロケールの日時を適切な形式で表します。
%x - ロケールの日付を適切な形式で表します。
%X - ロケールの時間を適切な形式で表します。

%G - ISO week(%V)の内過半数を含む西暦表記の ISO 8601 year です。
%u - １を月曜日を表す 10進数表記の ISO 8601 weekday です。
%V - 週で最初の月曜日を始めとする ISO 8601 week です。 Week 01 は１月４日を含みます。

%% - 文字 '%' を表します。

Linux ディストリビューションを使用したことがある場合は、このプロセスに精通している必要があります。\
''',

		'about_running_on': '{} での実行',
		'about_project_page': 'プロジェクトページ：',
		'about_beta_build': '\n警告：これはプレリリース バージョンであるため、バグやグリッチがある可能性があります。\n',
		'about_licensed': '{} ライセンスの下でライセンスされています',

		'bytes': 'バイト',

		'menubar_rbin_sid': 'あなたのSID：',
		'menubar_rbin_reload': 'ごみ箱をリロードする',
		'menubar_rbin_explorer_bin': 'ファイル エクスプローラでごみ箱を開く',
		'menubar_rbin_exit': '出口',
		'menubar_settings': '設定',
		'menubar_settings_rbin_view': 'ごみ箱ビュー',
		'menubar_settings_rbin_view_felike': 'ファイル エクスプローラーに似た',
		'menubar_settings_rbin_view_legacy': 'レガシー ビュー',
		'menubar_settings_sort_method': 'ファイルの並べ替え',
		'menubar_settings_sort_method_natsort': '自然な並べ替え',
		'menubar_settings_sort_method_lexico': '辞書式並べ替え',
		'menubar_settings_sort_method_folders_first': '最初にフォルダーを表示',
		'menubar_settings_dtformat': '日付と時刻の形式…',
		'menubar_settings_language': '言語',
		'menubar_settings_language_system': 'システム言語',
		'menubar_settings_language_info': '現在の言語の情報',
		'menubar_settings_locale': 'ロケール',
		'menubar_settings_locale_lang': '言語ロケール',
		'menubar_settings_locale_system': 'システム ロケール',
		'menubar_settings_locale_custom': 'カスタム',
		'menubar_settings_locale_custom2': '（{}）',
		'menubar_settings_updates': '更新',
		'menubar_settings_updates_auto': '起動時に更新を確認する',
		'menubar_settings_updates_prerelease': 'プレリリース バージョンを確認する',
		'menubar_help_update': '更新を確認する',
		'menubar_help_about': '{} について',

		'msgbox_error': 'エラー',
		'msgbox_warning': '警告',
		'msgbox_notice': '知らせ',
		'msgbox_no_formatting': 'この文字列にはフォーマットがありません。 とにかく続けます？',
		'msgbox_blank': 'この文字列を空白にすることはできません！',
		'msgbox_discard': '変更を破棄してもよろしいですか?',
		'msgbox_discard_item': '本当にこの項目を破棄しますか?',
		'msgbox_overwrite': 'ファイル {} は、元の場所に既に存在します。 上書きしますか？',
		'msgbox_error_unsupported_version': '：メタデータ ファイルのバージョンが不明またはサポートされていません',
		'msgbox_error_invalid_metadata': '：メタデータ ファイルが無効です',
		'msgbox_error_unicode': 'この文字列には、このバージョンの Tcl/Tk でサポートされていない Unicode 文字が含まれています。',
		'msgbox_unsupported_tcl': '一部の Unicode 文字をサポートしていないバージョンの Tcl/Tk を含む Python {} を実行しているようです。\n\n続けたいですか？',
		'msgbox_rbin_name_change': 'ごみ箱のファイル名の拡張子を、設定した新しい拡張子に更新しますか？\nそのままにしておくと、開いたときに「問題」が発生する可能性があります。',
		'msgbox_rbin_name_change_2': '「フォルダー」プロパティを変更するには、アイテムの古いデータを削除する必要があります。\n削除を続行しますか？ 「いいえ」を選択した場合、「フォルダ」プロパティは変更されません。',
		'msgbox_n_a': '未実装',
		'msgbox_n_a_desc': 'この機能は、このバージョンの {} には実装されていません。 ごめん！',
		'msgbox_reload_confirm': 'ごみ箱を再読み込みしてもよろしいですか？ このプロセスにより、メイン画面に戻ります。',
		'msgbox_reload_next_reboot': '次回プログラムを開いたときに、変更が有効になります。',
		'msgbox_not_in_rb': 'このアイテムはごみ箱にありません。\nこのリストから削除されます。',
		'msgbox_folder_warn': 'ごみ箱のフォルダーを開く場合、フォルダーが復元されるまでサブフォルダーを開くことはできません。\n\n続行しますか?',
		'msgbox_lnk_warn': '''\
開いたファイルはショートカット ファイル (.lnk) でした。

このショートカットがリンクしているファイルまたはフォルダーが存在しない場合、Windows はショートカットを削除するかどうかを尋ねるプロンプトを表示します。
[はい] を選択すると、ショートカットはごみ箱から完全に削除されます。

誤ってショートカットを開いてしまった場合でも、心配する必要はありません。「いいえ」 を押してください。

続けたいですか？\
''',
		'msgbox_restore': 'このアイテムを復元しますか？',
		'msgbox_restore_desc': 'このアイテムを元の場所に復元しますか?',
		'msgbox_restore_all': 'すべての項目を復元しますか?',
		'msgbox_restore_all_desc': 'ここにあるすべての項目を元の場所に復元しますか?',
		'msgbox_delete': 'この項目を削除しますか?',
		'msgbox_delete_desc': 'この項目を完全に削除してもよろしいですか?\nこれは、元に戻すことはできません！',
		'msgbox_delete_all': 'ごみ箱を空にする？',
		'msgbox_delete_all_desc': '削除済みアイテムをすべて消去してもよろしいですか?\n将来復元できない可能性があるため、これを行う前によく考えてください…',

		'ogname': '名前',
		'oglocation': '元の場所',
		'type': '種類',
		'size': 'サイズ',
		'deldate': '削除時間',
		'rbin_in': '{} のごみ箱',
		'discard': '破棄',
		'preview': 'プレビュー',
		'reset': '既定値にリセット',
		'help': 'ヘルプ',
		'edit': '編集',

		'back': '戻る',
		'cancel': 'キャンセル',

		'ftype_desc_folder': 'ファイル フォルダー',
		'ftype_desc_txt': 'テキスト ドキュメント',
		'ftype_desc_ini': '構成設定',
		'ftype_desc_ps1': 'Windows PowerShell スクリプト',
		'ftype_desc_ico': 'アイコン',
		'ftype_desc_file': 'ファイル',
		'ftype_desc_file': '{} ファイル',

		'main_loading': 'ごみ箱を読み込んでいます。 お待ちください…',
		'main_warning': '警告：',
		'main_rb_corrupt': 'ドライブ {} のごみ箱が破損しています。',
		'main_rbin_empty': 'ごみ箱が空です！',
		'main_rbin_metadata_unsupported_version': '知らせ：ごみ箱には、RBEditor が読み取れないメタデータ ファイルが含まれていました。',
		'main_new_item': '新しい項目',
		'main_restore_all': 'すべての項目を復元する',
		'main_empty_rb': 'ごみ箱を空にする',
		'main_open': '開く',
		'main_delete': '削除',
		'main_restore': '戻す',
		'main_properties': 'プロパティ',
		'main_folder': '《フォルダー》',

		'itemproperties_properties': '項目のプロパティ',
		'itemproperties_advanced': 'アドバンス情報',
		'itemproperties_reduced': '縮小情報',
		'itemproperties_ogname': '元の名前',
		'itemproperties_ogname_unterminated': '（終了文字なし）',
		'itemproperties_real_size': 'リアルサイズ',
		'itemproperties_size_disk': 'ごみ箱のサイズ',
		'itemproperties_metadata_size': 'メタデータ ファイルのサイズ',
		'itemproperties_rbin_name_i': 'ごみ箱のファイル名（メタデータファイル）',
		'itemproperties_rbin_name_r': 'ごみ箱のファイル名（データファイル）',
		'itemproperties_rbin_location': '場所',
		'itemproperties_version': 'メタデータ ファイルのバージョン',
		'itemproperties_version_text': 'バージョン',
		'itemproperties_location_asterisk': '* デスクトップからの相対パス',
		'itemproperties_location_asterisk_2': '** ファイル エクスプローラーでこのフォルダーの実際の内容にアクセスすることはできません',

		'new_item_edit': '既存の項目を編集',
		'new_item_path': '元のファイルパス',
		'new_item_folder': 'フォルダー？',
		'new_item_bytes_note': '（バイト単位）',
		'new_item_ext': '拡大',
		'new_item_name': '新しいごみ箱項目',
		'new_item_version_warning': 'このメタデータ ファイルのバージョンは、このバージョンの Windows では読み取ることができません。 それでも続行しますか？',
		'new_item_size_int_error': 'サイズは整数でなければなりません！',
		'new_item_size_out_of_range': 'サイズは -(2^63) から 2^63-1 の間でなければなりません。',
		'new_item_error_unsupported_version': '無効なメタデータファイルのバージョンです！',
		'new_item_invalid_path': 'ファイルパスに次の文字を含めることはできません：',
		'new_item_invalid_path_2': 'ファイルパスにはディレクトリを含める必要があります！',
		'new_item_invalid_path_3': 'ファイルパスが無効です！',
		'new_item_invalid_path_4': 'ファイルパスは絶対パスにする必要があります！',

		'new_item_hacker_mode': 'ハッカーモード',
		'new_item_hacker_mode_note': '（このエラーを回避するには、ハッカーモードを有効にしてください！）',
		'new_item_hacker_mode_enable': 'ハッカーモードを有効にする',
		'new_item_hacker_mode_no_terminator': '終端文字を持たないファイルパス（メタデータバージョン２のみ）',

		'locale_chooser_title': 'ロケールを選択',
		'locale_chooser_choose': 'ロケールを選択してください',

		'dtpicker_title': '日付と時刻のピッカー',
		'dtpicker_type': '入力種類',
		'dtpicker_type_basic': '基本',
		'dtpicker_day': '日',
		'dtpicker_month': '月',
		'dtpicker_year': '年',
		'dtpicker_hour': '時',
		'dtpicker_minute': '分',
		'dtpicker_second': '秒',
		'dtpicker_microsecond': 'マイクロ秒',
		'dtpicker_ft_header': '時刻（FILETIME形式）',
		'dtpicker_ft_learn_more': 'FILETIME について詳しく見る',
		'dtpicker_ft_int_error': 'FILETIME は整数でなければなりません！',
		'dtpicker_ft_out_of_range': 'FILETIME が有効な範囲内にありません！',

		'updater_title': 'アップデーター',
		'updater_checking': 'アップデートの確認…',
		'updater_donotclose': 'アップデートの確認中は\nプログラムを閉じないでください',
		'updater_exceeded': 'GitHub API のレート制限を超えました!\n後でもう一度やり直してください。',
		'updater_offline': 'インターネットに接続できません。インターネット\n接続が安定しているときにもう一度お試しください。',
		'updater_unknown_error': 'アップデートを確認できません！\n後でもう一度やり直してください。',
		'updater_newupdate_title': '利用可能なアップデート',
		'updater_newupdate': 'アップデートが利用可能です！',
		'updater_currver': '現行版：',
		'updater_newver': '新しいバージョン：',
		'updater_prerelease': '（プレリリース）',
		'updater_prompt': 'ダウンロードページに行きますか？',
		'updater_latest': 'すでに最新バージョンを使用しています。',
		'updater_download': 'ダウンロードページにアクセス',
	},
	'fr': {
		'info': '''\
Français - 4ème langue de RBEditor
(c) 2022-2023 GamingWithEvets Inc.\
''',

		'qmark': '?',

		'title': 'ÉDITEUR DE CORBEILLE - RBEditor',
		'title_dtformat': 'Formatage de la date et de l\'heure',
		'dtformat': 'Format de date et d\'heure',
		'dtformat_preview': 'À quoi ressemble votre format de date et d\'heure lorsqu\'il est utilisé:',
		'dtformat_guide': '''\
Source: https://docs.python.org/fr/3.6/library/datetime.html#strftime-and-strptime-behavior

%a - Jour de la semaine abrégé dans la langue locale.
%A - Jour de la semaine complet dans la langue locale.
%w - Jour de la semaine en chiffre, avec 0 pour le dimanche et 6 pour le samedi.

%d - Jour du mois sur deux chiffres.
%b - Nom du mois abrégé dans la langue locale.
%B - Nom complet du mois dans la langue locale.
%m - Numéro du mois sur deux chiffres.
%y - Année sur deux chiffres (sans le siècle).
%Y - Année complète sur quatre chiffres.

%H - Heure à deux chiffres de 00 à 23.
%I - Heure à deux chiffres pour les horloges 12h (01 à 12).
%p - Équivalent local à AM/PM.
%M - Minutes sur deux chiffres.
%S - Secondes sur deux chiffres.
%f - Microsecondes sur 6 chiffres.
%z - Décalage UTC sous la forme +HHMM ou -HHMM.
%Z - Nom du fuseau horaire.

%j - Numéro du jour dans l’année sur trois chiffres.
%U - Numéro de la semaine à deux chiffres (où dimanche est considéré comme le premier jour de la semaine). Tous les jours de l’année précédent le premier dimanche sont considérés comme appartenant à la semaine 0.
%W - Numéro de la semaine à deux chiffres (où lundi est considéré comme le premier jour de la semaine). Tous les jours de l’année précédent le premier lundi sont considérés comme appartenant à la semaine 0.

%c - Représentation locale de la date et de l’heure.
%x - Représentation locale de la date.
%X - Représentation locale de l’heure.

%G - Année complète ISO 8601 représentant l’année contenant la plus grande partie de la semaine ISO (%V).
%u - Jour de la semaine ISO 8601 où 1 correspond au lundi.
%V - Numéro de la semaine ISO 8601, avec lundi étant le premier jour de la semaine. La semaine 01 est la semaine contenant le 4 janvier.

%% - Un caractère '%' littéral.

Si vous avez utilisé une distribution Linux, vous devez être familiarisé avec ce processus.\
''',

		'about_running_on': 'Exécution sur {}',
		'about_project_page': 'Page du projet: ',
		'about_beta_build': '\nAVERTISSEMENT: Il s\'agit d\'une pré-version, elle peut donc contenir des bogues et/ou des problèmes.\n',
		'about_licensed': 'Licencié sous la licence {}',

		'bytes': 'octet(s)',
		'KB': 'Ko',
		'KiB': 'Kio',
		'MB': 'Mo',
		'MiB': 'Mio',
		'GB': 'Go',
		'GiB': 'Gio',
		'TB': 'To',
		'TiB': 'Tio',
		'PB': 'Po',
		'PiB': 'Pio',
		'EB': 'Eo',
		'EiB': 'Eio',
		'ZB': 'Zo',
		'ZiB': 'Zio',
		'YB': 'Yo',
		'YiB': 'Yio',

		'menubar_rbin_sid': 'Votre SID: ',
		'menubar_rbin_reload': 'Recharger la Corbeille',
		'menubar_rbin_explorer_bin': 'Ouvrir la Corbeille dans l\'Explorateur de fichiers',
		'menubar_rbin_exit': 'Quitter',
		'menubar_settings': 'Paramètres',
		'menubar_settings_rbin_view': 'Vue Corbeille',
		'menubar_settings_rbin_view_felike': 'Similaire à l\'Explorateur de fichiers',
		'menubar_settings_rbin_view_legacy': 'Ancienne vue',
		'menubar_settings_sort_method': 'Tri de fichiers',
		'menubar_settings_sort_method_natsort': 'Tri naturel',
		'menubar_settings_sort_method_lexico': 'Tri lexicographique',
		'menubar_settings_sort_method_folders_first': 'Afficher les dossiers en premier',
		'menubar_settings_dtformat': 'Formatage de la date et de l\'heure...',
		'menubar_settings_language': 'Langue',
		'menubar_settings_language_system': 'Langue du système',
		'menubar_settings_language_info': 'Infos pour la langue actuelle',
		'menubar_settings_locale': 'Paramètres régionaux',
		'menubar_settings_locale_lang': 'Paramètres régionaux de la langue',
		'menubar_settings_locale_system': 'Paramètres régionaux du système',
		'menubar_settings_locale_custom': 'Coutume',
		'menubar_settings_locale_custom2': ' ({})',
		'menubar_settings_updates': 'Mises à jour',
		'menubar_settings_updates_auto': 'Vérifier les mises à jour au démarrage',
		'menubar_settings_updates_prerelease': 'Vérifier les versions préliminaires',
		'menubar_help_update': 'Vérifier les mises à jour',
		'menubar_help_about': 'À propos de {}',

		'msgbox_error': 'Erreur',
		'msgbox_warning': 'Avertissement',
		'msgbox_notice': 'Avis',
		'msgbox_no_formatting': 'Cette chaîne de caractères n\'a pas de formatage. Continuer quand même?',
		'msgbox_blank': 'Cette chaîne de caractères ne peut pas être vide!',
		'msgbox_discard': 'Voulez-vous vraiment annuler vos modifications?',
		'msgbox_discard_item': 'Êtes-vous sûr de vouloir supprimer cet élément?',
		'msgbox_overwrite': 'Le fichier {} existe déjà à son emplacement d\'origine. Voulez-vous l\'écraser?',
		'msgbox_error_unsupported_version': ': Version de fichier de métadonnées inconnue ou non prise en charge',
		'msgbox_error_invalid_metadata': ': Fichier de métadonnées non valide',
		'msgbox_error_unicode': 'Cette chaîne de caractères contient des caractères Unicode non pris en charge par cette version de Tcl/Tk.',
		'msgbox_unsupported_tcl': 'Il semble que vous exécutiez Python {}, qui a une version de Tcl/Tk qui ne prend pas en charge certains caractères Unicode.\n\nVoulez-vous continuer?',
		'msgbox_rbin_name_change': 'Voulez-vous mettre à jour l\'extension du nom de fichier de la Corbeille avec la nouvelle que vous avez définie?\nSi vous le laissez tel quel, vous pourriez voir des "problèmes" lors de son ouverture.',
		'msgbox_rbin_name_change_2': 'La modification de la propriété "Dossier" nécessitera la suppression des anciennes données de l\'élément.\nSouhaitez-vous poursuivre la suppression? Si vous sélectionnez Non, la propriété "Dossier" ne changera pas.',
		'msgbox_n_a': 'Pas mis en œuvre',
		'msgbox_n_a_desc': 'Cette fonctionnalité n\'est pas implémentée dans cette version de {}. Désolé!',
		'msgbox_reload_confirm': 'Voulez-vous vraiment recharger la Corbeille? Vous reviendrez au menu principal.',
		'msgbox_reload_next_reboot': 'Les modifications prendront effet la prochaine fois que vous ouvrirez le programme.',
		'msgbox_not_in_rb': 'Cet article n\'est plus dans la Corbeille.\nIl sera désormais supprimé de cette liste.',
		'msgbox_folder_warn': 'Lors de l\'ouverture d\'un dossier dans la Corbeille, vous ne pouvez ouvrir aucun sous-dossier tant que le dossier n\'est pas restauré.\n\nVoulez-vous continuer?',
		'msgbox_lnk_warn': '''\
Le fichier que vous avez ouvert était un fichier de raccourci (.lnk).

Si le fichier ou le dossier auquel ce raccourci renvoie n'existe plus, Windows affichera une invite vous demandant si vous souhaitez supprimer le raccourci.
Si vous sélectionnez Oui, le raccourci sera PERMANENTEMENT SUPPRIMÉ de la Corbeille.

Si vous avez ouvert le raccourci par accident, ne vous inquiétez pas, appuyez simplement sur Non.

Voulez-vous continuer?\
''',
		'msgbox_restore': 'Restaurer cet élément?',
		'msgbox_restore_desc': 'Voulez-vous restaurer cet élément à son emplacement d\'origine?',
		'msgbox_restore_all': 'Restaurer tous les éléments?',
		'msgbox_restore_all_desc': 'Voulez-vous restaurer tous les éléments ici à leur emplacement d\'origine?',
		'msgbox_delete': 'Supprimer cet élément?',
		'msgbox_delete_desc': 'Êtes-vous sûr de vouloir supprimer définitivement cet élément?\nVOUS NE POUVEZ PAS ANNULER CECI!',
		'msgbox_delete_all': 'Vider la Corbeille?',
		'msgbox_delete_all_desc': 'Êtes-vous sûr de vouloir effacer tous vos éléments supprimés?\nRéfléchissez bien avant de faire cela, car vous ne pourrez peut-être pas les récupérer à l\'avenir...',

		'ogname': 'Nom',
		'oglocation': 'Emplacement d\'origine',
		'type': 'Type',
		'size': 'Taille',
		'deldate': 'Heure de suppression',
		'rbin_in': 'Corbeille dans {}',
		'discard': 'Jeter',
		'preview': 'Prévisualisation',
		'reset': 'Rétablir les paramètres par défaut',
		'help': 'Aider',
		'edit': 'Modifier',

		'back': 'Dos',
		'cancel': 'Annuler',

		'ftype_desc_folder': 'Dossier de fichiers',
		'ftype_desc_txt': 'Document texte',
		'ftype_desc_ini': 'Paramètres de configuration',
		'ftype_desc_ps1': 'Script Windows PowerShell',
		'ftype_desc_ico': 'Icon',
		'ftype_desc_file': 'Fichier',
		'ftype_desc_file_space': 'Fichier {}',

		'main_loading': 'Chargement de la Corbeille, veuillez patienter...',
		'main_warning': 'AVERTISSEMENT:',
		'main_rb_corrupt': 'La Corbeille sur le lecteur {} est corrompue.',
		'main_rbin_empty': 'La Corbeille est vide!',
		'main_rbin_metadata_unsupported_version': 'REMARQUE: Votre Corbeille contient des fichiers de métadonnées que RBEditor ne peut pas lire.',
		'main_new_item': 'Nouvel élément',
		'main_restore_all': 'Restaurer tous les éléments',
		'main_empty_rb': 'Vider la Corbeille',
		'main_open': 'Ouvrir',
		'main_delete': 'Supprimer',
		'main_restore': 'Restaurer',
		'main_properties': 'Propriétés',
		'main_folder': '<dossier>',

		'itemproperties_properties': 'Propriétés de l\'élément',
		'itemproperties_advanced': 'Informations avancées',
		'itemproperties_reduced': 'Infos réduites',
		'itemproperties_ogname': 'Nom d\'origine',
		'itemproperties_ogname_unterminated': '(chaîne de caractères non terminée)',
		'itemproperties_real_size': 'Taille réelle',
		'itemproperties_size_disk': 'Taille dans la Corbeille',
		'itemproperties_metadata_size': 'Taille du fichier de métadonnées',
		'itemproperties_rbin_name_i': 'Nom de fichier dans la Corbeille (fichier de métadonnées)',
		'itemproperties_rbin_name_r': 'Nom de fichier dans la Corbeille (fichier de données)',
		'itemproperties_rbin_location': 'Emplacement',
		'itemproperties_version': 'Version du fichier de métadonnées',
		'itemproperties_version_text': 'Version ',
		'itemproperties_location_asterisk': '* Les chemins relatifs partent du Bureau',
		'itemproperties_location_asterisk_2': '** Vous ne pouvez pas accéder au contenu réel de ce dossier avec l\'Explorateur de fichiers',

		'new_item_edit': 'Modifier l\'élément existant',
		'new_item_path': 'Chemin du fichier d\'origine',
		'new_item_folder': 'Dossier?',
		'new_item_bytes_note': '(en octets)',
		'new_item_ext': 'Extension',
		'new_item_name': 'Nouvel élément de la Corbeille',
		'new_item_version_warning': 'Cette version du fichier de métadonnées ne peut pas être lue par cette version de Windows. Continuer quand même?',
		'new_item_size_int_error': 'La taille doit être un entier!',
		'new_item_size_out_of_range': 'La taille doit être comprise entre -(2^63) et 2^63-1',
		'new_item_error_unsupported_version': 'Version du fichier de métadonnées non valide!',
		'new_item_invalid_path': 'Le chemin du fichier ne doit pas contenir les caractères suivants:',
		'new_item_invalid_path_2': 'Le chemin du fichier doit inclure des répertoires!',
		'new_item_invalid_path_3': 'Chemin de fichier invalide!',
		'new_item_invalid_path_4': 'Le chemin du fichier doit être absolu!',

		'new_item_hacker_mode': 'Mode hacker',
		'new_item_hacker_mode_note': '(pour contourner cette erreur, activez le mode hacker!)',
		'new_item_hacker_mode_enable': 'Activer le mode hacker',
		'new_item_hacker_mode_no_terminator': 'Chemin d\'accès au fichier non terminé (métadonnées version 2 uniquement)',

		'locale_chooser_title': 'Sélection de paramètres régionaux',
		'locale_chooser_choose': 'Sélectionnez un paramètre régional:',

		'dtpicker_title': 'Sélecteur de date et d\'heure',
		'dtpicker_type': 'Type d\'entrée',
		'dtpicker_type_basic': 'Basique',
		'dtpicker_day': 'Jour',
		'dtpicker_month': 'Mois',
		'dtpicker_year': 'Année',
		'dtpicker_hour': 'Heures',
		'dtpicker_minute': 'Minutes',
		'dtpicker_second': 'Secondes',
		'dtpicker_microsecond': 'Microsecondes',
		'dtpicker_ft_header': 'Heure (format FILETIME)',
		'dtpicker_ft_learn_more': 'En savoir plus sur FILETIME',
		'dtpicker_ft_int_error': 'FILETIME doit être un entier!',
		'dtpicker_ft_out_of_range': 'FILETIME n\'est pas dans la plage valide!',

		'updater_title': 'Actualisateur',
		'updater_checking': 'Vérification des mises à jour...',
		'updater_donotclose': 'NE PAS fermer le programme lors\nde la recherche de mises à jour',
		'updater_exceeded': 'Limite de débit de l\'API GitHub dépassée!\nVeuillez réessayer plus tard.',
		'updater_offline': 'Impossible de se connecter à internet. Veuillez\nréessayer lorsque vous disposerez d\'une connexion\nInternet stable.',
		'updater_unknown_error': 'Impossible de vérifier les mises à jour!\nVeuillez réessayer plus tard.',
		'updater_newupdate': 'Une mise à jour est disponible!',
		'updater_currver': 'Version actuelle: ',
		'updater_newver': 'Nouvelle version:  ',
		'updater_prerelease': ' (pré-version)',
		'updater_latest': 'Vous utilisez déjà la dernière version.',
		'updater_download': 'Visite la page de téléchargement',
	},
}
