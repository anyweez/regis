///////////////////////////////////////////////////
////// Backbone models / views / collections //////
///////////////////////////////////////////////////

/// Cards ///

var CardType = Backbone.Model.extend({});
var CardTypeView = Backbone.View.extend({
   tagName: 'div',
   className: 'card',

   events : {
	   'click h2' : 'local_activate'
   },
   
   initialize: function() {
      $('#card-stack').append(this.el);
   },
   
   // Activates this card in the deck that' currently active.
   local_activate : function() {
	   regis.getActiveDeck().activate(this.model);
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
	
	activate: function(target_card) {
		that = this;
		this.each(function(card, index) {
			if (target_card.get('card_id') == card.get('card_id')) {
				that.aci = index;
				that.view.update();
			}
		});
	},

	deactivateActive: function() {
	  this.aci = null;
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

// Collection to hold all of the decks.
var DeckCollectionType = Backbone.Collection.extend({
    collection: DeckType
});

// View for a single deck to generate icon view.
var DeckTypeIconView = Backbone.View.extend({
  tagName: 'li',
  className: 'deck-icon',
  
  initialize: function() {
    $('#deck-bench-list').append(this.el);
  },

  render: function() {
	icon_html = "<p>" + this.collection.name + "</p>";
	icon_html += "<p>(" + this.collection.length + ")</p>";
	
	if (this.collection.length < 10) {
		$(this.el).addClass('deck-size-lg');
	}
	else if (this.collection.length < 20) {
		$(this.el).addClass('deck-size-med');
	}
	else {
		$(this.el).addClass('deck-size-lg');		
	}
	
    $(this.el).html(icon_html);
    $(this.el).css('display', 'inline-block');
    return this;
  },
});

// Render the views for all of the deck icons.  This only needs to be
// called once.
var DeckCollectionTypeView = Backbone.View.extend({
  tagName: 'div',
  className: 'deck-zone',
  id: 'deck-zone',

  initialize: function() {
    $('#deck-icons').append(this.el);
  },
  
  render: function() {
    $(this.el).html("<p id='deck-bench-label'>Your Decks</p><ul style='display: inline;' id='deck-bench-list'>");  
    $(this.el).css('display', 'block');
    $(this.el).css('position', 'absolute');
    $(this.el).css('top', '10px');
    $(this.el).css('left', '20px');

    return this;
  }
});

var DeckTypeView = Backbone.View.extend({
	initialize: function() {
//		this.on('click', this.activate, this);
		var that = this;
//		this._questionViews = [];

		this.collection.each(function(card) {
			qv = new CardTypeView({model: card});
//			that._questionViews.push(qv);
			
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
	
	showAll: function() {
	  this.collection.aci = null;
	  this.collection.each(function(card, index) {
		    $(card.view.el).show();
		    $(card.view.el).css({'z-index' : index});
		    $(card.view.el).animate({ 'top' : (15 * index) + 32 + '%', 'left' : '20%' });
	  });
	},
	
	update: function() {
	  if (this.collection.aci == null) return;

	  var that = this;
      // Move all of the invisible cards to the right side of the active
	  // question.  This prevents cards zooming around in the background.
	  this.collection.each(function(card, index) {
		var aci = that.collection.aci;
	    // Move eastward.
	    if (index - aci > 2) {
	      $(card.view.el).hide();
	      $(card.view.el).css({'left' : '160%', 'top' : '32%'});
	    }
	    // Move westward.
	    else if (index - aci < -2) {
	      $(card.view.el).hide();
	      $(card.view.el).css({'left' : '-120%', 'top' : '32%'});
	    }
	  });
	  
      // Move cards according to their relative placement to the active card.
      this.collection.each(function(card, index) {
  		var aci = that.collection.aci;
  		
        if (index == aci - 2) {
          $(card.view.el).css({'z-index' : 1});
          $(card.view.el).show();
          $(card.view.el).animate({ 'left' : '-120%', 'top' : '32%' }, 500);
        }
        // The element before the current element should appear on the left.
        if (index == aci - 1) {
          $(card.view.el).css({'z-index' : 2});
          $(card.view.el).show();
          $(card.view.el).animate({ 'left' : '-50%', 'top' : '32%' }, 500);
        }
        // The focus element should appear in the middle.
        else if (index == aci) {
          $(card.view.el).css({'z-index' : 3});
          $(card.view.el).show();
          $(card.view.el).animate({ 'left' : '20%', 'top' : '32%' }, 500);
        }
        // The element beyond the current element should appear on the right.
        else if (index == aci + 1) {
          $(card.view.el).css({'z-index' : 2});
          $(card.view.el).show();
          $(card.view.el).animate({ 'left' : '90%', 'top' : '32%' }, 500);
        }
        else if (index == aci + 2) {
          $(card.view.el).css({'z-index' : 1});
          $(card.view.el).show();
          $(card.view.el).animate({ 'left' : '160%', 'top' : '32%' }, 500);
        }
      });
	}
});

function regis_init() {
  /// Regis API code ///
  regis = (function() {
    var activeDeck = null;
  
    // Maybe we could use this collection to get the list of decks from the server?
    var deckCollection = new DeckCollectionType();
    var decks = {};
    var dctv = new DeckCollectionTypeView({collection: deckCollection});
  
    dctv.render();
    deckCollection.view = dctv;
  
    return {
      Deck: function(deck_name, deck_endpoint) {
        var deck = new DeckType(deck_endpoint);
        deck.name = deck_name;
      
        deck.fetch({ success: function(target_deck) {
          target_deck.view = new DeckTypeView({collection: target_deck});
          target_deck.icon = new DeckTypeIconView({collection: target_deck});
        
   	  	  // Set the active card to the first one
   	  	  if (target_deck.length > 0) {
   			target_deck.aci = 0;
   		  }
   	  	  
   		  // Render the deck's icon view.
		  target_deck.icon.render();
   		  target_deck.ready = true;

          deckCollection.add(target_deck);
          // Store the deck locally.
          decks[deck_endpoint] = deck;
   	    }}, deck);
      
        return deck;
    },
    
    getActiveDeck : function() {
    	return activeDeck;
    },
  
    activateDeck : function(target_deck) {
	  // Hide the currently active deck.
	  if (activeDeck != null) {
	    activeDeck.view.hide();
	  }
	
	  // Show the newly activated deck and save it as the active deck.
  	  target_deck.view.update();
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
        else if (key.keyCode == 32) {
          activeDeck.view.showAll();
        }
        activeDeck.view.update();
      }
    },
  };
})();

$(document).ready(function() {
  $(document).bind('keydown', regis.keyResponse);
});
}

