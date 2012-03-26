///////////////////////////////////////////////////
////// Backbone models / views / collections //////
///////////////////////////////////////////////////

/// Cards ///

var CardType = Backbone.Model.extend({});
var CardTypeView = Backbone.View.extend({
   tagName: 'div',
   className: 'card',

   initialize: function() {
      $('#card-stack').append(this.el);
   },

   render: function() {
      $(this.el).html(this.model.get('html'));
      $(this.el).css('display', 'none');
      $(this.el).css('position', 'absolute');
      $(this.el).css('top', '180px');
      $(this.el).css('left', '250px');
      return this;
   },
   
   show: function() {
      $(this.el).css('display', 'block');
   },  
    
   hide: function() {
      $(this.el).css('display', 'none');
   },

   setCollectionView: function(view) {
      this.collectionView = view;
   },
});

/// Decks ///

var DeckType = Backbone.Collection.extend({
	model: CardType,
	url: '/api/decks/',
	ready: false,
	aci: null,									// active card index
	
	initialize: function(deck_name) {
	  this.url = this.url + deck_name;
	},
	
	updateView: function() {
	  _.each(this.models, function(card) {
	    card.view.hide();
	  });
      this.models[this.aci].view.show();
	},
	
	incrActive: function() {
	  if (this.aci != null) {
        if (this.aci + 1 >= this.length) {
          this.aci = 0;
        }
        else {
          this.aci++;
        }
	  }
	  else if (this.length > 0) {
	    this.aci = 0;
	    console.log('Activating first card');
	  }
	  else {
	    console.log('No card to activate');
	  }
      this.updateView();
	},
	
	decrActive: function() {
	  if (this.aci != null) {
        if (this.aci - 1 < 0) {
          this.aci = this.length - 1;
        }
        else {
          this.aci--;
        }
	  }
	  else if (this.length > 0) {
	    this.aci = 0;
	    console.log('Activating first card');
	  }
	  else {
	    console.log('No card to activate');
	  }
      this.updateView();
	},
});

var DeckTypeView = Backbone.View.extend({
	initialize: function() {
		var that = this;
		this._questionViews = [];
		this.activeQuestion = null;

		this.collection.each(function(card) {
			qv = new CardTypeView({model: card});
			that._questionViews.push(qv);
			
			card.view = qv;
			
			qv.setCollectionView(that);
			qv.render();
		});
	},
	
	show: function() {
		this.collection.each(function(card) {
			card.view.show();
		});
	},
		
	hide: function() {
		this.collection.each(function(card) {
			card.view.hide();
		});
	},
	
});

/// Regis API code ///
var regis = (function() {
  var activeDeck = null;
  var decks = {};
    
  return {
    Deck: function(deck_name) {
      var deck = new DeckType(deck_name);
      
      deck.fetch({ success: function() {
        dtv = new DeckTypeView({collection: deck});
        dtv.on('change:activeQuestion', function(model, text) {
     	  console.log('Active question: ' + text);
   		});
   		
   		// Set the active card to the first one
   		if (deck.length > 0) {
   			dtv.activeCard = 0;
   		}
   		deck.view = dtv;
   		deck.ready = true;
   	  }});
    
      // Store the deck locally.
      decks[deck_name] = deck;
      
      return deck;
    },
  
    activateDeck : function(target_deck) {
	  // Hide the currently active deck.
	  if (activeDeck != null) {
	    activeDeck.view.hide();
	  }
	
	  // Show the newly activated deck and save it as the active deck.
  	  target_deck.view.show();
  	  activeDeck = target_deck;
    },
    
    keyResponse : function(key) {
      if (activeDeck != null) {
        // right arrow key
        if (key.keyCode == 39) {
          activeDeck.incrActive();
        }
        // left arrow key
        else if (key.keyCode == 37) {
          activeDeck.decrActive();
        }
      }
    },
  };
})();

$(document).ready(function() {
  $(document).bind('keydown', regis.keyResponse);
});