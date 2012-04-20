///////////////////////////////////////////////////
////// Backbone models / views / collections //////
///////////////////////////////////////////////////

/// Cards ///
/**
 * The base class for a single card.  These are constructed based
 * on the data received in the CardListType.  They can be constructed
 * manually as well, although it shouldn't really be necessary.
 * 
 * The only field the card requires is the 'html' field, which is the
 * data that is directly injected into the card's body.
 */
var CardType = Backbone.Model.extend({
	guess_base_url: '/api/answer/',
	
	submit_guess : function(guess_val) {
		guess_url = this.guess_base_url + this.get('question_id');
		console.log('Submitting guess (' + guess_val + ') to ' + guess_url);
		
		that = this;
		$.ajax({
			url: guess_url,
			type: 'POST',
			data: {
				'guess' : guess_val
			},
			success: function(response) {
				that.update_on_guess(response);
			}
		});
	},
	
	update_on_guess : function(response) {
		console.log('updating card #' + this.get('question_id'));
		if (response.hasOwnProperty('error')) {
			console.log('Error! ' + response.error);
		}
		else if (response.hasOwnProperty('correct')) {
			console.log('Correct? ' + response.correct);
			if (response.correct) {
				$(this.view.el).find('h2').css('background-color', '#009933');
				$(this.view.el).find('h2').css('border-bottom', '1px solid black');
			}
			else {
				$(this.view.el).find('h2').effect("highlight", { 'color' : '#ff0000' }, 2000);
			}
		}
	},
});

/**
 * The view for a single CardType.
 */
var CardTypeView = Backbone.View.extend({
   tagName: 'div',
   className: 'card',

   events : {
	   'click h2' : 'local_activate',
	   'click input[type=button]' : 'submit_guess',
   },
   
   initialize: function() {
      $('#card-stack').append(this.el);
      
      _.bindAll(this);
   },
   
   submit_guess: function() {
	   this.model.submit_guess($(this.el).find(':input[type=text]').val());
   },
   
   // Activates this card in the deck that's currently active.
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

   // TODO (luke): can we get rid of setCollectionView?
   setCollectionView: function(view) {
      this.collectionView = view;
   },
});

/**
 * Keeps track of all cards that are viewable by the user.  This is the
 * single source of truth; all questions that the user can view are stored
 * here.  Individual cards are added to decks based on this list.
 */
var CardListType = Backbone.Collection.extend({
	model: CardType,
	url: '/api/questions',
	ready: false
});

/// Decks ///
/**
 * A single deck, which contains a series of cards from a CardListType.
 * The endpoint that this model pulls from provides a list of card id's
 * that are then used to add the correct cards to the deck (this step
 * currently occurs in the callback for the fetch() method).  
 * 
 * The deck also keeps track of which card is 'active' in order to make
 * it possible to store different values per deck.
 */
var DeckType = Backbone.Collection.extend({
	model: CardType,
	url: '/api/decks',
	ready: false,
	aci: null,									// active card index
	
	initialize: function(deck_name) {
	  if (deck_name != null) this.url = this.url + '/' + deck_name;

	  _.bindAll(this);
	},
	
	activate: function(target_card) {
		that = this;
		old_aci = this.aci;
		this.each(function(card, index) {
			if (target_card.get('card_id') == card.get('card_id')) {
				that.aci = index;
				// TODO: Check to make sure that this deck is active before doing this.
				if (old_aci != that.aci) that.view.update();
			}
		});
	},

	deactivateActive: function() {
	  this.aci = null;
	},
	
	incrActive: function() {
      // Nothing we can do in this case.
	  if (this.length == 0) return;
	  // If there isn't an active card, set the first card as the new
      // active card.
	  if (this.aci == null && this.length > 0) this.aci = 0;
	  // If there is an active card and we're overflowing, wrap around
	  // to the beginning.
	  else if (this.aci + 1 >= this.length) this.aci = 0;
	  // Otherwise, increment normally.
      else this.aci++;

	  this.view.update();
	},
	
	decrActive: function() {
      // No cards, no service.
      if (this.length == 0) return;
      // No active card, start at the back.
      if (this.aci == null && this.length > 0) this.aci = this.length - 1;
      // Wrap around to the back.
      else if (this.aci - 1 < 0) this.aci = this.length - 1;
      // Otherwise just decrease by one.
      else this.aci--;

      this.view.update();
	},
});

// Collection to hold all of the decks.
var DeckCollectionType = Backbone.Collection.extend({
    collection: DeckType,
	url: '/api/decks',

	parse: function(response) {
	  var models = [];
	  console.log('Parsing decks from server.');
          response.reverse();
          response.push({'deck_id' : -1, 'name' : 'All', 'members' : []});
          response.reverse();
	  _.each(response, function(deck_opt) {
		  var new_deck = new DeckType();

		  new_deck.name = deck_opt.name;
		  new_deck.deck_id = deck_opt.deck_id;
		  
		  regis.getCardList().each(function(card, index) {
			  if ((deck_opt.name == 'All' && deck_opt.deck_id == -1) ||
                                  deck_opt.members != undefined && 
				  deck_opt.members.indexOf(card.get('question_id')) > -1) {

//				  if (card.view == null) card.view = new CardTypeView({model: card});
				  new_deck.add(card);
			  }
		  });
		  
		  console.log('  Added ' + new_deck.size() + ' cards to deck "' + new_deck.name + '"');

   	  	  // Set the active card to the first one
		  new_deck.aci = (new_deck.length > 0) ? 0 : null;
		  
		  // Define the views that go along with this deck.
		  new_deck.view = new DeckTypeView({collection: new_deck});
		  new_deck.icon = new DeckTypeIconView({
			  collection: new_deck, 
			  add_to_shelf: true
		  });

		  new_deck.forEach(function(card) {
			 card.view.render(); 
		  });
		  
		  new_deck.on('add', new_deck.icon.render);
		  new_deck.on('remove', new_deck.icon.render);
		  new_deck.on('remove', new_deck.view.update);
   		  // Render the deck's icon view.
		  new_deck.icon.render();
		  new_deck.ready = true;
		  
		  models.push(new_deck);
	  });
	  console.log('Done.');
	  
	  return models;
	},
});

// View for a single deck to generate icon view.
var DeckTypeIconView = Backbone.View.extend({
  tagName: 'li',
  className: 'deck-icon',
  
  events : {
	  'click' : 'activate'
  },
  
  initialize: function(deck_opts) {
    // Add the deck to the shelf as long as the user doesn't specify otherwise
	// via setting add_to_shelf = false.
	add_to_shelf = (deck_opts.add_to_shelf == null) ? true : deck_opts.add_to_shelf; 
	console.log('Adding deck to shelf? ' + add_to_shelf);
    if (add_to_shelf) $('#deck-icons').append(this.el);
    
    _.bindAll(this);
  },

  activate: function() {
	  regis.activateDeck(this.collection);
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
	
	// Fade the decks that don't have anything in them.
	if (this.collection.length == 0) $(this.el).css('opacity', '.4');
	else $(this.el).css('opacity', '1');
	
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
    $(this.el).css('line-height', '.5em');
    $(this.el).css('padding-bottom', '0px');

    return this;
  }
});

var DeckTypeView = Backbone.View.extend({
	draggable: true,
	
	initialize: function() {
		var that = this;
		// If the user specified that the card *shouldn't* be draggable, flip
		// the flag.
		if (this.options.draggable === false) this.draggable = this.options.draggable;

		this.collection.each(function(card) {
			if (card.view == undefined) card.view = new CardTypeView({model: card});
			if (that.draggable) $(card.view.el).addClass('draggable');

			card.view.setCollectionView(that);
			card.view.render();
		});
		
		_.bindAll(this);
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
	
	render: function() {
		this.collection.forEach(function(card) {
			if (card.view == null) card.view = new CardTypeView({model: card});
			card.view.render();
		})
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
	      $(card.view.el).css({'left' : '160%', 'top' : '26%'});
	    }
	    // Move westward.
	    else if (index - aci < -2) {
	      $(card.view.el).hide();
	      $(card.view.el).css({'left' : '-120%', 'top' : '26%'});
	    }
	  });
	  
      // Move cards according to their relative placement to the active card.
	  this.collection.each(function(card, index) {
  		var aci = that.collection.aci;

  		console.log(card);
        if (index == aci - 2) {
          $(card.view.el).css({'z-index' : 1});
          $(card.view.el).show();
          $(card.view.el).animate({ 'left' : '-120%', 'top' : '26%' }, 500);
        }
        // The element before the current element should appear on the left.
        else if (index == aci - 1) {
          $(card.view.el).css({'z-index' : 2});
          $(card.view.el).show();
          $(card.view.el).animate({ 'left' : '-50%', 'top' : '26%' }, 500);
        }
        // The focus element should appear in the middle.
        else if (index == aci) {
          $(card.view.el).css({'z-index' : 3});
          $(card.view.el).show();
          $(card.view.el).animate({ 'left' : '20%', 'top' : '26%' }, 500);
        }
        // The element beyond the current element should appear on the right.
        else if (index == aci + 1) {
          $(card.view.el).css({'z-index' : 2});
          $(card.view.el).show();
          $(card.view.el).animate({ 'left' : '90%', 'top' : '26%' }, 500);
        }
        else if (index == aci + 2) {
          $(card.view.el).css({'z-index' : 1});
          $(card.view.el).show();
          $(card.view.el).animate({ 'left' : '160%', 'top' : '26%' }, 500);
        }
      });
	}
});

/**
 * The view for a single CardType.
 */
var CardTypeView = Backbone.View.extend({
   tagName: 'div',
   className: 'card',

   events : {
	   'click h2' : 'local_activate',
	   'submit #answerbox' : 'submit_guess',
   },
   
   initialize: function() {
      $('#card-stack').append(this.el);
      
      _.bindAll(this);
   },
   
   submit_guess: function() {
	   this.model.submit_guess($(this.el).find(':input[name=answer]').val());
	   return false;
   },
   
   // Activates this card in the deck that's currently active.
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

   // TODO (luke): can we get rid of setCollectionView?
   setCollectionView: function(view) {
      this.collectionView = view;
   },
});

function initialize_ui() {
	$('.draggable').each(function(index, el) {
		$(el).draggable({ 
		  cancel: ':input,button,p',
		  distance: 30,
		  revert: true,
		  start: function(event, ui) {
		    console.log('dragging');
		    $(el).css('opacity', '.6');
		  },
		  stop: function(event, ui) {
		    $(el).css('opacity', '1');
		  },
		});
	});

	$('.deck-icon').each(function(index, el) {
		$(el).droppable({ 
		  tolerance: 'pointer',
		  activate: function(event, ui) {
			console.log('activated dragging (droppable noticed)');  
		  },
			
		  drop: function(event, ui) {
		    console.log('dropped onto icon');
	        $(this).css('background-color', 'transparent');
		    // this = droppable
		    // ui.draggable = draggable
	        
	        // Add draggable to droppable
	        regis.addCardToDeck(ui.draggable[0], this);
		  },
		  
		  over: function(event, ui) {
            $(this).css('background-color', 'yellow');
		  },
		  
		  out: function(event, ui) {
	        $(this).css('background-color', 'transparent');
		  }
		});
	});
	
	$('.card-close-btn').each(function(index, el) {
		$(el).click(function(event) {
			regis.removeCardFromDeck($(el).parent());
		})
	});
}

/**
 * The starter function that takes care of initial data requests and provides
 * the client-side API for loading and managing cards and decks.
 * 
 * This function should be called after the document has been loaded but before
 * any other Regis API code usage.
 */
function regis_init(regis_opts) {
  /// Regis API code ///
  regis = (function() {
    var activeDeck = null;
    var cardList = new CardListType();
    
    var dc = new DeckCollectionType();
    var dctv = new DeckCollectionTypeView({collection: dc});

    // Re-render the DCTV whenever a new deck is added.
    dctv.on('add', dctv.render);
    dc.view = dctv;    
    
    // If the deck should be loaded during initialization, go for it.
    if (regis_opts != null && 'load_full' in regis_opts && regis_opts['load_full']) {
    	// Fetch all questions from the server.
    	cardList.fetch( { success: function() {
    		cardList.ready = true;
    		
    		dc.fetch({ success: function() {
    			dc.view.render();
    			initialize_ui();
    		}});
    	}});
    }
    
    return {
      Deck: function(deck_opts) {
        var deck = ('endpoint' in deck_opts) ? new DeckType(deck_opts['endpoint']) : new DeckType();

        if ('name' in deck_opts) deck.name = deck_opts['name'];
        deck.aci = null;

        deck.view = new DeckTypeView({collection: deck, draggable: false});
        deck.icon = new DeckTypeIconView({
          collection: deck, 
          add_to_shelf: ('add_to_shelf' in deck_opts) ? deck_opts['add_to_shelf'] : true,
        });
        
//		deck.on('add', deck.icon.render);
//		deck.on('remove', deck.icon.render);
//		deck.on('remove', deck.view.update);
        
        if (deck.icon.options.add_to_shelf) {
        	console.log('Adding deck "' + deck.name + '" to shelf');
        	dc.add(deck);
        }

        // Only do a remote fetch if there's an endpoint specified.
        if ('endpoint' in deck_opts) {
          deck.fetch({ success: function(target_deck) {
        	// Render the views now that all of the data is loaded.
        	target_deck.view.render();
            if (target_deck.icon.options.add_to_shelf) target_deck.icon.render();            

              // Set the active card to the first one
   	  	    if (target_deck.length > 0) target_deck.aci = 0;
   	  	  
   		    // Render the deck's icon view.
   		    target_deck.ready = true;
   	      }}, deck);
        }
        else {
        	// No data is coming right away...render now!
            deck.view.render();
            if (deck.icon.options.add_to_shelf) deck.icon.render();

            deck.ready = true;
        }
		
        return deck;
    },
    
    getActiveDeck : function() {
    	return activeDeck;
    },
    
    getCardList : function() {
    	return cardList;
    },
    
    getDeckCollection: function() {
    	return dc;
    },

    // Pass in HTML elements.  We need to scan through to determine which (a) card
    // and (b) deck the elements are referring to.  This should be able to be O(1)
    // if I can figure out a way to store card ID's in the HTML...maybe using
    // jQuery's data() call.  
    // TODO (luke): optimize addCardToDeck() in clientside API.
    addCardToDeck: function(in_card, in_deck) {
      var target_card = null;
      var target_deck = null;
      activeDeck.each(function(current_card) {
    	  if (current_card.view.el == in_card) target_card = current_card;
      });
      
      regis.getDeckCollection().each(function(current_deck) {
    	  if (current_deck.attributes.icon.el == in_deck) target_deck = current_deck.attributes;
      });
      
      try {
    	  target_deck.add(target_card);
    	  // Send a POST request so that the server gets the update.  There's
    	  // probably a more Backbone-y way to do this, possibly overriding
    	  // sync() for DeckType, but I haven't been able to figure that
    	  // out yet.
    	  // TODO (luke): Try to integrate deck updating w/ Backbone.
    	  $.ajax({
    	    type: 'put',
    	    url: '/api/decks/' + target_deck.deck_id + '/questions/' + target_card.get('question_id'), // TODO(from cartland for Luke): target_card.get('card_id') = undefined
          });
      }
      catch (err) {
    	  console.log('[Warning] That card already exists in the specified deck.');
      }
    },
    
    // Removes out_card from the active deck.
    removeCardFromDeck: function(out_card) {
    	var target_card = null;
    	var target_index = null;
    	
        activeDeck.each(function(current_card, index) {
      	  if (current_card.view.el == out_card[0]) {
      		  target_card = current_card;
      		  target_index = index;
      	  }
        });
        
        if (target_card != null) {
        	activeDeck.view.hide();
        	activeDeck.remove(target_card);

        	// This could likely also be integrated into the Backbone framework somehow.
      	    // TODO (luke): Try to integrate deck updating w/ Backbone.
      	    $.ajax({
      	      type: 'delete',
    	      url: '/api/decks/' + activeDeck.deck_id + '/questions/' + '1',// target_card.get('card_id'), // TODO(from cartland for Luke): target_card.get('card_id') = undefined
            });
      	  
        	if (activeDeck.aci == target_index) {
        		activeDeck.incrActive();
        	}
        }
    },
    
    activateDeck : function(target_deck) {
      console.log('Switching to deck "' + target_deck.name + '" (size: ' + target_deck.size() + ')');
	  // Hide the currently active deck.
	  if (activeDeck != null) {
	    activeDeck.view.hide();
	  }

	  // Show the newly activated deck and save it as the active deck.
	  // TODO: bug occurs here! Apr 5, 2012
  	  target_deck.view.update();
  	  target_deck.view.show();
  	  activeDeck = target_deck;
    },
    
    keyResponse : function(key) {
      var earlyActive = activeDeck;
      if (activeDeck != null) {
        var updated = false;
    	// right arrow key
        if (key.keyCode == 39) activeDeck.incrActive();
        // left arrow key
        else if (key.keyCode == 37) activeDeck.decrActive();
        // space bar
        else if (key.keyCode == 32) activeDeck.view.showAll();
        
        // update the deck's view if anything changed
        if (earlyActive != activeDeck) activeDeck.view.update();
      }
    },
  };
})();

  $(document).ready(function() {
    $(document).bind('keydown', regis.keyResponse);
  });
}

