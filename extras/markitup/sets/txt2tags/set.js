// -------------------------------------------------------------------
// markItUp!
// -------------------------------------------------------------------
// Copyright (C) 2009 Florent Gallaire <fgallaire@gmail.com>  
// License GNU GPLv3 or any later version.
// Copyright (C) 2008 Jay Salvat
// http://markitup.jaysalvat.com/
// -------------------------------------------------------------------
// Txt2tags tags example
// http://txt2tags.org/markup.html
// -------------------------------------------------------------------
// Feel free to add more tags
// -------------------------------------------------------------------
mySettings = {
	previewParserPath:	'', // path to your Txt2tags parser
	onShiftEnter:		{keepDefault:false, replaceWith:'\n\n'},
	markupSet: [
		{name:'Heading 1', key:'1', openWith:'= ', closeWith:' =', placeHolder:'Your title here...' },
		{name:'Heading 2', key:'2', openWith:'== ', closeWith:' ==', placeHolder:'Your title here...' },
		{name:'Heading 3', key:'3', openWith:'=== ', closeWith:' ===', placeHolder:'Your title here...' },
		{name:'Heading 4', key:'4', openWith:'==== ', closeWith:' ====', placeHolder:'Your title here...' },
		{name:'Heading 5', key:'5', openWith:'===== ', closeWith:' =====', placeHolder:'Your title here...' },
		{separator:'---------------' },		
		{name:'Bold', key:'B', openWith:'**', closeWith:'**'}, 
		{name:'Italic', key:'I', openWith:'//', closeWith:'//'}, 
		{name:'Underline', key:'U', openWith:'__', closeWith:'__'}, 
		{name:'Strike', key:'S', openWith:'--', closeWith:'--'}, 
		{separator:'---------------' },
		{name:'Bulleted list', openWith:'- '}, 
		{name:'Numeric list', openWith:'+ '}, 
		{separator:'---------------' },
		{name:'Picture', key:'P', openWith:'[', closeWith:']', placeHolder:'Your picture here...'}, 
		{name:'Link', key:'L', openWith:'[', closeWith:' [![Link:!:http://]!]]', placeHolder:'Your text to link here...'},
		{separator:'---------------'},	
		{name:'Quote', openWith:'\t'},
		{name:'Code', openWith:'``', closeWith:'``'},
		{name:'Raw', key:'R', openWith:'""', closeWith:'""', placeHolder:'No txt2tags in here!'},		
		{separator:'---------------' },
		{name:'Preview', call:'preview', className:'preview'}
	]
}
