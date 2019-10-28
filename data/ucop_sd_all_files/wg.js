function loadSearchResults()
{
	jQuery(document).ready(function()
	{ 
		jQuery("#list2").jqGrid({
			url:'search.action',
			mtype: 'POST', 
			datatype: 'json',
		   	colNames:['Id', 'Year','Location','First<br/>Name','Last<br/>Name','Title','Gross<br/>Pay','Regular<br/>Pay','Overtime<br/>Pay','OtherPay'],
		   	colModel:[
		   		{name:'Id',index:'RNUM', width:10, hidden: true},
		   		{name:'Year',index:'EAW_YR', width:28},
		   		{name:'Location',index:'EAW_LOC_NAM', width:60},
		   		{name:'FirstName',index:'EAW_FST_NAM', width:80},
		   		{name:'LastName',index:'EAW_LST_NAM', width:80},
		   		{name:'Title',index:'EAW_TTL_SHRT_NAM', width:160},
		   		{name:'GrossPay',index:'EAW_GRS_EARN_AMT', width:80, formatter:'number', formatoptions: {thousandsSeparator:','}, align:'right'},
		   		{name:'BasePay',index:'EAW_BS_PY_AMT', width:80,formatter:'number', formatoptions: {thousandsSeparator:','},align:'right'},
		   		{name:'Overtime',index:'EAW_OVERTM_EARN_AMT', width:60, formatter:'number', formatoptions: {thousandsSeparator:','},align:'right'},
		   		{name:'Other',index:'EAW_ADJT_AMT', width:80, formatter:'number', formatoptions: {thousandsSeparator:','},align:'right'}
		   	],
		   	rowNum:20,
		   	width:'100%',
		   	height:'100%',
		   	rowList:[20,40,60],
		   	pager: '#pager2',
		   	sortname: 'EAW_LST_NAM',
		    sortorder: "ASC",
		    sortable: true,
		    rownumbers: true,
		    viewrecords: true,
		    hidegrid: false,
			rownumWidth: 28,
		    caption:"Search Results",
		    loadComplete: function () {
			    if($('#list2').getGridParam("records")==0) { 
					$("#noResultsDiv").show();   
				}
		    },
		    loadError: function (jqXHR, textStatus, errorThrown) 
		    {         
		    	//alert('HTTP status code: ' + jqXHR.status + '\n textStatus: ' + textStatus + '\n errorThrown: ' + errorThrown);
		    	if (textStatus=="error") {
		    		//alert(jqXHR.responseText);
		    		$("#errorDiv").show();
		    		$("#list2").hide();
		    		$("#pager2").hide();
			    	
				}    	
		    } 
		});
		
		jQuery("#list2").jqGrid('navGrid','#pager2',{add:false,edit:false,del:false,search:false,refresh:true,view:true});
		
			$('#showGrossPay').click(function(){     
		          $('#grosspay').dialog({modal:true, title: 'Other Pay / Adjustment category', width: 500 });     
		      });
	}); 
}

function showResults()
{
	var dt = $('#sform').serializeArray();   
	$.each(dt,function(i, field){
		//alert(field.name+"="+field.value);
		$("#list2").setPostDataItem(field.name, field.value);
	});
	//$("#list2").trigger("reloadGrid"); 
	$("#noResultsDiv").hide(); 
	$("#errorDiv").hide(); 
	$("#list2").trigger("reloadGrid", [{page:1}]);
	var yr = document.sform.year.value;
	//alert(yr);
	if( yr < 2013){	
			jQuery("#list2").jqGrid('setLabel', 8, 'Base<br/>Pay');
			jQuery("#list2").jqGrid('setLabel', 10, 'OtherPay/<br/>Adjstmt');
			
		}else{
			jQuery("#list2").jqGrid('setLabel', 8, 'Regular<br/>Pay');
			jQuery("#list2").jqGrid('setLabel', 10, 'OtherPay');
		
		} 
	return true;
}

function validate()
{
	var errmsg="";
	var loc = document.sform.location.value;
	var fname = document.sform.firstname.value;
	var lname = document.sform.lastname.value;
	var titlef = document.sform.title.value;
	var stSal = document.sform.startSal.value;
	var enSal = document.sform.endSal.value; 
	if (loc=='') {errmsg=errmsg+"Please select a location";}
	if (loc=="ALL" && fname=='' && lname =='' && titlef=='' && stSal=='' && enSal==''){
		errmsg="You have selected to search ALL locations. Please enter additional search criteria. \n";
	}
	if (stSal!=null) {stSal=trim(stSal);}
	if (enSal!=null) {enSal=trim(enSal);}
	if (isNaN(stSal) || isNaN(enSal)) {errmsg=errmsg+"Salary range should be numeric\n";}
	if (stSal.length==0 && enSal.length>0) {document.sform.startSal.value="0";}
	if (enSal.length==0 && stSal.length>0) {document.sform.endSal.value="9999999";}
	if (errmsg.length==0) {
	   if (parseInt(stSal) > parseInt(enSal)) {
			errmsg=errmsg+"Salary range: start value can not be less than end value \n";
		}
	}

	if (errmsg.length>0) {
		alert(errmsg);
		return false;
	}
	else {
		return true;
	}
}

function trim(s)
{
	var l=0; var r=s.length -1;
	while(l < s.length && s[l] == ' ')
	{	l++; }
	while(r > l && s[r] == ' ')
	{	r-=1;	}
	return s.substring(l, r+1);
}

$(function() {
		$("button", ".actionbutton").button();
	});
	
function displayLocList()
{
	var yr = document.sform.year.value;
	var loccombo=document.sform.location;
	if (yr < 2013){
		//alert(yr);
		for (m=loccombo.options.length;m>0;m--){
			loccombo.options[m]=null;
		}
		loccombo.options[0] = new Option("Select a Location","");
		loccombo.options[1] = new Option("Berkeley","Berkeley");
		loccombo.options[2] = new Option("DANR","DANR");
		loccombo.options[3] = new Option("Davis","Davis");
		loccombo.options[4] = new Option("Irvine","Irvine");
		loccombo.options[5] = new Option("Los Angeles","Los Angeles");
		loccombo.options[6] = new Option("Merced","Merced");
		loccombo.options[7] = new Option("Riverside","Riverside");
		loccombo.options[8] = new Option("San Diego","San Diego");
		loccombo.options[9] = new Option("San Francisco","San Francisco");
		loccombo.options[10] = new Option("Santa Barbara","Santa Barbara");
		loccombo.options[11] = new Option("Santa Cruz","Santa Cruz");
		loccombo.options[12] = new Option("UCOP","UCOP");
		loccombo.options[13] = new Option("ALL","ALL");
		loccombo.options[0].selected=true;
		document.getElementById('notes2012').style.display = "block";
		document.getElementById('notes').style.display = "none";
	} 
	else if ((2012 < yr) && (yr < 2018)){
		for (m=loccombo.options.length;m>0;m--){
			loccombo.options[m]=null;
		}
		loccombo.options[0] = new Option("Select a Location","");
		loccombo.options[1] = new Option("Berkeley","Berkeley");
		loccombo.options[2] = new Option("Davis","Davis");
		loccombo.options[3] = new Option("Irvine","Irvine");
		loccombo.options[4] = new Option("Los Angeles","Los Angeles");
		loccombo.options[5] = new Option("Merced","Merced");
		loccombo.options[6] = new Option("Riverside","Riverside");
		loccombo.options[7] = new Option("San Diego","San Diego");
		loccombo.options[8] = new Option("San Francisco","San Francisco");
		loccombo.options[9] = new Option("Santa Barbara","Santa Barbara");
		loccombo.options[10] = new Option("Santa Cruz","Santa Cruz");
		loccombo.options[11] = new Option("UCOP","UCOP");
		loccombo.options[12] = new Option("ALL","ALL");
		loccombo.options[0].selected=true;
		document.getElementById('notes2012').style.display = "none";
		document.getElementById('notes').style.display = "block";
	}
	else{
		for (m=loccombo.options.length;m>0;m--){
				loccombo.options[m]=null;
		}
		loccombo.options[0] = new Option("Select a Location","");
		loccombo.options[1] = new Option("ASUCLA","ASUCLA");
		loccombo.options[2] = new Option("Berkeley","Berkeley");
		loccombo.options[3] = new Option("Davis","Davis");
		loccombo.options[4] = new Option("Hastings","Hastings College Of Law");
		loccombo.options[5] = new Option("Irvine","Irvine");
		loccombo.options[6] = new Option("Los Angeles","Los Angeles");
		loccombo.options[7] = new Option("Merced","Merced");
		loccombo.options[8] = new Option("Riverside","Riverside");
		loccombo.options[9] = new Option("San Diego","San Diego");
		loccombo.options[10] = new Option("San Francisco","San Francisco");
		loccombo.options[11] = new Option("Santa Barbara","Santa Barbara");
		loccombo.options[12] = new Option("Santa Cruz","Santa Cruz");
		loccombo.options[13] = new Option("UCOP","UCOP");
		loccombo.options[14] = new Option("ALL","ALL");
		loccombo.options[0].selected=true;
		document.getElementById('notes2012').style.display = "none";
		document.getElementById('notes').style.display = "block";
	}
}