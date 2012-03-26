var Question = Backbone.Model.extend({});
var QuestionView = Backbone.View.extend({
   tagName: 'div',
   className: 'card',

   initialize: function() {
      $(this.el).data('card-id', this.model.id);
      $('#card-stack').append(this.el);
   },

   render: function() {
      $(this.el).html("<h2 data-card-id='" + this.model.get('id') + 
                      "' class='title'>" + this.model.get('title') + 
                      "</h2><p class='body_text'>" + this.model.get('text') + "</p>");
      $(this.el).css('display', 'block');
      return this;
   },

   setCollectionView: function(view) {
      this.collectionView = view;
      $(this.el).bind('click', this.collectionView.clickActivate);
   },
});

/*
var Profile = Backbone.Model.extend({});
var ProfileView = Backbone.View.extend({
   events: {},
   tagName: 'div',
   className: 'card',

   initialize: function() {
      $('#card-stack').append(this.el);
   },

   render: function() {
//      $(this.el).html("<h2 class='title'>" + this.model.get('name') + "</h2><p class='body_text'>" + this.model.get('percentage') + "% complete</p>");
      $(this.el).html("<h2 class='title'>Title!</h2>");
      $(this.el).css('display', 'block');
      return this;
   },
});

var profile = new Profile({
   name: 'Tom Sawyer', 
   percentage: 89
});

var profileView = new ProfileView({model: profile});
profileView.render();
*/

//////////////////////////////////////////////////
//////////////////////////////////////////////////
//////////////////////////////////////////////////

var QuestionList = Backbone.Collection.extend({
   model: Question,
   url: '/api/questions/fakelist'
});

var QuestionListView = Backbone.View.extend({
   test: 5,
   initialize: function() {
      var that = this;
      this._questionViews = [];
      this.activeQuestion = null;
  
      this.collection.each(function(card) {
         qv = new QuestionView({model: card});
         that._questionViews.push(qv);

         qv.setCollectionView(that);

         $(qv.el).css({
            'display': 'none', 
            'position' : 'absolute'
         });
         qv.render();
      });

      _.bindAll(this, 'keyResponse');
      _.bindAll(this, 'clickActivate');
      $(document).bind('keydown', this.keyResponse);
   },

   keyResponse: function(key) {
      // Right arrow key
      if (key.keyCode == 39) {
         this.incrActive()
         this.adjustView();
         console.log('Active question: ' + this.activeQuestion);
      }
      // Left arrow key
      else if (key.keyCode == 37) {
         this.decrActive();
         this.adjustView();
         console.log('Active question: ' + this.activeQuestion);
      }
      // Space key -- current deactivates all questions.
      else if (key.keyCode == 32) {
         this.hideIfActive();
         this.deactivate();
         console.log('Deactivating questions');
         this.showAll();
      }
      // P for profile
      else if (key.keyCode == 80) {
//         this.showProfile();
//         console.log('Showing profile....');
      }
   },

   showAll: function() {
      this.activeQuestion = null;
      $.each(this._questionViews, function(index, view) {
         $(view.el).show();
         $(view.el).css({'z-index' : index});
         $(view.el).animate({ 'top' : (15 * index) + 32 + '%', 'left' : '20%' });
      });      
   },

   clickActivate: function(view) {
      for (field in view.toElement) {
         console.log(field);
      }
      if (this.activeQuestion == null) {
         qlv.activeQuestion = $(view.toElement).data('card-id');
         qlv.adjustView();
      }
   },

   adjustView: function() {
      var that = this;
      console.log('Updating view (active card= #' + this.activeQuestion + ')...');

      // Move all of the invisible cards to the right side of the active
      // question.  This prevents cards zooming around in the background.
      $.each(this._questionViews, function(index, view) {
         // Move eastward.
         if (index - that.activeQuestion > 2) {
            $(view.el).hide();
            $(view.el).css({'left' : '160%', 'top' : '32%'});
         }
         // Move westward.
         else if (index - that.activeQuestion < -2) {
            $(view.el).hide();
            $(view.el).css({'left' : '-120%', 'top' : '32%'});
         }
      });

      // Move cards according to their relative placement to the active card.
      $.each(this._questionViews, function(index, view) {
         if (index == that.activeQuestion - 2) {
            $(view.el).css({'z-index' : 1});
            $(view.el).show();
            $(view.el).animate({ 'left' : '-120%', 'top' : '32%' }, 500);
         }
         // The element before the current element should appear on the left.
         if (index == that.activeQuestion - 1) {
            $(view.el).css({'z-index' : 2});
            $(view.el).show();
            $(view.el).animate({ 'left' : '-50%', 'top' : '32%' }, 500);
         }
         // The focus element should appear in the middle.
         else if (index == that.activeQuestion) {
            $(view.el).css({'z-index' : 3});
            $(view.el).show();
            $(view.el).animate({ 'left' : '20%', 'top' : '32%' }, 500);
         }
         // The element beyond the current element should appear on the right.
         else if (index == that.activeQuestion + 1) {
            $(view.el).css({'z-index' : 2});
            $(view.el).show();
            $(view.el).animate({ 'left' : '90%', 'top' : '32%' }, 500);
         }
         else if (index == that.activeQuestion + 2) {
            $(view.el).css({'z-index' : 1});
            $(view.el).show();
            $(view.el).animate({ 'left' : '160%', 'top' : '32%' }, 500);
         }
         // All elements other than the central three should be hidden.
         else {
//            $(view.el).css({'z-index' : 1});
         }
      });
   },
/*
   showProfile: function() {
      this.hideIfActive();
      this.profileView.render();
   },
*/
   deactivate: function() {
      this.activeQuestion = null;
   },

   hideIfActive: function() {
      if (this.activeQuestion != null) {
         $(this._questionViews[this.activeQuestion].el).css('display', 'none');
      }
//      $(profileView.el).css('display', 'none');
   },

   incrActive: function() {
      // If we're switching to a single-card view from list view.
      if (this.activeQuestion == null && this._questionViews.length > 0) {
         this.activeQuestion = 0;
//         this._questionViews[this.activeQuestion].render();
      }
      // If we're moving from one card to another without looping back to the
      // beginning of the deck (i.e. most cases).
      else if (this._questionViews.length > this.activeQuestion + 1) {
         this.activeQuestion += 1;
//         this._questionViews[this.activeQuestion].render();
      }
      // If we're looping back to the beginning.
      else if (this._questionViews.length > 0) {
         this.activeQuestion = 0;
//         this._questionViews[this.activeQuestion].render();
      }
      // If something's not right here.
      else {
         alert('Cannot increment');
      }
   },

   decrActive: function() {
      // If we're switching to a single-card view from list view.
      if (this.activeQuestion == null && this._questionViews.length > 0) {
         this.activeQuestion = 0;
         this._questionViews[this.activeQuestion].render();
      }
      // If we're looping back to the end.
      else if (this.activeQuestion - 1 < 0) {
//         this.set({activeQuestion: this._questionViews.length - 1});
         this.activeQuestion = this._questionViews.length - 1;
         this._questionViews[this.activeQuestion].render();
      }
      // If we're moving from one card to another without looping back to the
      // beginning of the deck (i.e. most cases).
      else {
         this.activeQuestion -= 1;
         this._questionViews[this.activeQuestion].render();
      }
   },

   render: function() {
      if (this.activeQuestion) {
         this._questionViews.at(this.activeQuestion).render();
      }
      else {
         alert('No question active.');
      }
   }
});

/*
var QuestionViewListView = Backbone.View.extend({
   events: {},
   tagname: 'div',
   className: 'card-stack',
   id: 'card-stack',

   initialize: function() {},

   render: function() {
      for (i = 0; i < this.model.length; i++) {
         console.log(this.model.at(i).get('text'));
         this.model.at(i).render();
      }
   }
});
*/

//question.on('change:text', function(model, text) {
//   $('#question-body').html('<b>' + text + '</b');
//});

var questionlist = new QuestionList;
var qlv = null;

questionlist.fetch({ success: function() { 
   qlv = new QuestionListView({collection: questionlist});
   qlv.on('change:activeQuestion', function(model, text) {
     console.log('Active question: ' + text);
   });

   qlv.activeQuestion = 0;
   qlv.adjustView();
 }
})

