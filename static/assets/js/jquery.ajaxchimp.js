/*!
Mailchimp Ajax Submit
jQuery Plugin
Author: Siddharth Doshi

Use:
===
$('#form_id').ajaxchimp(options);

- Form should have one <input> element with attribute 'type=email'
- Form should have one label element with attribute 'for=email_input_id' (used to display error/success message)
- All options are optional.

Options:
=======
options = {
    language: 'en',
    callback: callbackFunction,
    url: 'http://blahblah.us1.list-manage.com/subscribe/post?u=5afsdhfuhdsiufdba6f8802&id=4djhfdsh99f'
}

Notes:
=====
To get the mailchimp JSONP url (undocumented), change 'post?' to 'post-json?' and add '&c=?' to the end.
For e.g. 'http://blahblah.us1.list-manage.com/subscribe/post-json?u=5afsdhfuhdsiufdba6f8802&id=4djhfdsh99f&c=?',
*/
!function(a) {
    "use strict";
    a.ajaxChimp = {
        responses: {
            "We have sent you a confirmation email": 0,
            "Please enter a value": 1,
            "An email address must contain a single @": 2,
            "The domain portion of the email address is invalid (the portion after the @: )": 3,
            "The username portion of the email address is invalid (the portion before the @: )": 4,
            "This email address looks fake or invalid. Please enter a real email address": 5
        },
        translations: {
            en: null
        },
        init: function(e, s) {
            a(e).ajaxChimp(s)
        }
    },
    a.fn.ajaxChimp = function(e) {
        return a(this).each(function(s, n) {
            var i = a(n)
              , t = i.find("input[type=email]")
              , r = i.find("label[for=" + t.attr("id") + "]")
              , l = a.extend({
                url: i.attr("action"),
                language: "en"
            }, e)
              , o = l.url.replace("/post?", "/post-json?").concat("&c=?");
            i.attr("novalidate", "true"),
            t.attr("name", "EMAIL"),
            i.submit(function() {
                function e(e) {
                    if ("success" === e.result)
                        s = "We have sent you a confirmation email",
                        r.removeClass("error").addClass("valid"),
                        t.removeClass("error").addClass("valid");
                    else {
                        t.removeClass("valid").addClass("error"),
                        r.removeClass("valid").addClass("error");
                        var n = -1;
                        try {
                            var i = e.msg.split(" - ", 2);
                            if (void 0 === i[1])
                                s = e.msg;
                            else {
                                var o = parseInt(i[0], 10);
                                o.toString() === i[0] ? (n = i[0],
                                s = i[1]) : (n = -1,
                                s = e.msg)
                            }
                        } catch (m) {
                            n = -1,
                            s = e.msg
                        }
                    }
                    "en" !== l.language && void 0 !== a.ajaxChimp.responses[s] && a.ajaxChimp.translations && a.ajaxChimp.translations[l.language] && a.ajaxChimp.translations[l.language][a.ajaxChimp.responses[s]] && (s = a.ajaxChimp.translations[l.language][a.ajaxChimp.responses[s]]),
                    r.html(s),
                    r.show(2e3),
                    l.callback && l.callback(e)
                }
                var s, n = {}, m = i.serializeArray();
                a.each(m, function(a, e) {
                    n[e.name] = e.value
                }),
                a.ajax({
                    url: o,
                    data: n,
                    success: e,
                    dataType: "jsonp",
                    error: function(a, e) {
                        console.log("mailchimp ajax submit error: " + e)
                    }
                });
                var u = "Submitting...";
                return "en" !== l.language && a.ajaxChimp.translations && a.ajaxChimp.translations[l.language] && a.ajaxChimp.translations[l.language].submit && (u = a.ajaxChimp.translations[l.language].submit),
                r.html(u).show(2e3),
                !1
            })
        }),
        this
    }
}(jQuery);
