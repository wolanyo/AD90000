 openerp.benin_petro = function (openerp)
{  
//=====================================================================================================================================
openerp.web.form.widgets.add('statistique_stat_client', 'openerp.benin_petro.stat_client');
    openerp.benin_petro.stat_client = openerp.web.form.FieldChar.extend({
        template : "statistique_stat_client",
//openerp.notaire_statistique.categories

//=====================================================================================================================================



//=====================================================================================================================================
openerp.web.form.widgets.add('statistique_stat_client_recharhe', 'openerp.benin_petro.stat_client_recharhe');
    openerp.benin_petro.stat_client_recharhe = openerp.web.form.FieldChar.extend({
        template : "statistique_stat_client_recharhe",
//=======
	//var Model = require('web.Model') 
        init: function (view, code) {
		this._super(view, code);
		var ds = new openerp.web.DataSet(this, 'benin_petro.statistique_client', {});
		$(".o_control_panel").css("display","none");
		
		
        },// fiiiiiiiiiiiiiiiiiiiiiiiin init
//======
	start: function() {
		var ds = new openerp.web.DataSet(this, 'benin_petro.statistique_client', {});
		//var Model = require('web.Model') 
	// ***************************************
		var client = "All";
		var year = "All";
		var month = "All";
		ds.call('getAllYear', [ds]).done(function(data) {
			$('#yearValue').html(data);
		})
		ds.call('getAllMonth', [ds]).done(function(data) {
			$('#monthValue').html(data);
		})
		
		ds.call('getClient', [ds]).done(function(data) {
			$("#clients_recharge").html(data);

		});
		ds.call('getListeRechargeClient', [ds,client,year,month,$("#datedebut").val(),$("#datefin").val()]).done(function(data) {
			$("#table_result_recharge").html(data.table);
			$('#result_datatable_recharge').dataTable().fnDestroy();
			$('#result_datatable_recharge').dataTable({
			      dom: 'Bfrtip',
				buttons: [
				{
					extend: 'pdfHtml5', 
					text: 'Exporter en PDF', 
					title: function(){
							 return "Liste des recharges clients"
						      },
					  footer: true ,
					   customize: function (doc) {
			   					doc.content[1].table.widths = 
						Array(doc.content[1].table.body[0].length + 1).join('*').split('');
			  		}
				}
				],
 			      "sScrollY": "450px",
			      "sScrollX": "100%",
			      "sScrollXInner": "100%",
			      "bScrollCollapse": true,
			      "fixedHeader": true,
			      "bPaginate": true,
				  "ordering": true,
				  "searching": true,
				  "info": true,
				  "autoWidth": true,
				  "iDisplayLength": 5,
				  "pagingType": "full_numbers",
				  "language": {
				  "search": "Recherche:",
				  "info":"Affichage de l'&eacute;lement _START_ &agrave; _END_ sur _TOTAL_ &eacute;l&eacute;ments",
				    "paginate": {
				      "next": ">",
				      "previous": "<",
				      "first": "<<",
				      "last": ">>"
				    },
				  "emptyTable": "Aucune donn&eacute;e disponible dans le tableau"
				}
			});

		});


		$("body").on("change",".select_recharge",function(){
			
			year = $("#yearValue").val();
			month = $("#monthValue").val();
			ds.call('getListeRechargeClient', [ds,$("#clients_recharge").val(),year,month,$("#datedebut").val(),$("#datefin").val()]).done(function(data) {
				$("#table_result_recharge").html(data.table);
				$('#result_datatable_recharge').dataTable().fnDestroy();
				$('#result_datatable_recharge').dataTable({
				      dom: 'Bfrtip',
					buttons: [
					{
						extend: 'pdfHtml5', 
						text: 'Exporter en PDF', 
						title: function(){
								 return "Liste des recharges clients"
							      },
						  footer: true ,
						   customize: function (doc) {
				   					doc.content[1].table.widths = 
							Array(doc.content[1].table.body[0].length + 1).join('*').split('');
				  		}
					}
					],
	 			      "sScrollY": "450px",
				      "sScrollX": "100%",
				      "sScrollXInner": "100%",
				      "bScrollCollapse": true,
				      "fixedHeader": true,
				      "bPaginate": true,
					  "ordering": true,
					  "searching": false,
					  "info": true,
					  "autoWidth": true,
					  "iDisplayLength": 5,
					  "pagingType": "full_numbers",
					  "language": {
					  "search": "Recherche:",
					  "info":"Affichage de l'&eacute;lement _START_ &agrave; _END_ sur _TOTAL_ &eacute;l&eacute;ments",
					    "paginate": {
					      "next": ">",
					      "previous": "<",
					      "first": "<<",
					      "last": ">>"
					    },
					  "emptyTable": "Aucune donn&eacute;e disponible dans le tableau"
					}
				});
				
			});
		})
		

		 
	
	
	// ***************************************
	},// fiiiiiiiiiiiiiiiiiiiiiiiiin start
//======
    });//openerp.notaire_statistique.categories

// //=====================================================================================================================================














































}
