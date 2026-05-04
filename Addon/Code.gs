function buildAddOn(e) {
  const card = CardService.newCardBuilder()
    .setHeader(
      CardService.newCardHeader()
        .setTitle("Malicious Email Scorer")
        .setSubtitle("Analyze the opened email")
    )
    .addSection(
      CardService.newCardSection()
        .addWidget(
          CardService.newTextParagraph()
            .setText("Click the button below to analyze this email.")
        )
        .addWidget(
          CardService.newTextButton()
            .setText("Analyze Email")
            .setOnClickAction(
              CardService.newAction().setFunctionName("analyzeEmail")
            )
        )
    )
    .build();

  return card;
}




function analyzeEmail(e) {
  const url = "https://purplish-culminate-street.ngrok-free.dev/analyze";

  const accessToken = e.gmail.accessToken;
  const messageId = e.gmail.messageId;

  const message = GmailApp.getMessageById(messageId);

  const subject = message.getSubject();
  const sender = message.getFrom();
  const body = message.getPlainBody();

  const payload = {
    subject: subject,
    sender: sender,
    reply_to: sender,
    body: body
  };

  const options = {
    method: "post",
    contentType: "application/json",
    payload: JSON.stringify(payload)
  };

  const response = UrlFetchApp.fetch(url, options);
  const data = JSON.parse(response.getContentText());

  const card = CardService.newCardBuilder()
    .setHeader(CardService.newCardHeader().setTitle("Analysis Result"))
    .addSection(
      CardService.newCardSection()
        .addWidget(
          CardService.newTextParagraph().setText(
            `<b>Score:</b> ${data.score}<br>
             <b>Verdict:</b> ${data.verdict}<br><br>
             <b>Reasons:</b><br>- ${data.reasons.join("<br>- ")}`
          )
        )
    )
    .build();

  return card;
}