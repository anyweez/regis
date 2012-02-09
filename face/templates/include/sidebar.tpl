    <div id="right_col">
      <div id="small_right">
        <h3>{{ user.username }}</h3>
        <div class="statbox">
          <!-- question count progress bar -->
          <div id="qc_pb" class="progress_bar"></div>
          <p style="font-size: small; margin: 0; padding: 0; margin-bottom: 24px; color: #555;">{{ stats.percent_answered }}% of available questions answered</p>
        </div>

		<div class="statbox">
		  <h2>Questions Answered</h2>
		  <p>{{ stats.questions_answered.0 }} of {{ stats.questions_answered.1 }}</p>
		</div>
		<div class="statbox">
		  <h2>Guesses per Question</h2>
		  <p>{{ stats.guesses_per_question }}</p>
		</div>
		<div class="statbox">
		  <h2>Fastest Answer</h2>
		  <p>{{ stats.fastest_answer }}</p>
		</div>
		<div class="statbox">
		  <h2>Hardest Question Answered</h2>
		  <p style="margin-bottom: 0px; padding-bottom: 0px; font-style: italic;">{{ stats.hardest_question_answered.0.template.title }}</p>
		  <p style="color: #444; font-size: small; margin-top: 2px;">answered by {{ stats.hardest_question_answered.1 }}%</p>
		</div>
      </div>
    </div> 
