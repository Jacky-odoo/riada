odoo.define('attachment_activity_done.attachment', function (require) {
"use strict";

    var core = require('web.core');
    require('mail.Activity');

    var mailUtils = require('mail.utils');
    var _t = core._t;
    var _lt = core._lt;
    var ajax = require('web.ajax');
    var field_registry = require('web.field_registry');
    var Activity = field_registry.get('mail_activity');
    var framework = require('web.framework');
    var session = require('web.session');
    var time = require('web.time');
    var QWeb = core.qweb;

    var setDelayLabel = function (activities){
        var today = moment().startOf('day');
        _.each(activities, function (activity){
            var toDisplay = '';
            var diff = activity.date_deadline.diff(today, 'days', true); // true means no rounding
            if (diff === 0){
                toDisplay = _t("Today");
            } else {
                if (diff < 0){ // overdue
                    if (diff === -1){
                        toDisplay = _t("Yesterday");
                    } else {
                        toDisplay = _.str.sprintf(_t("%d days overdue"), Math.abs(diff));
                    }
                } else { // due
                    if (diff === 1){
                        toDisplay = _t("Tomorrow");
                    } else {
                        toDisplay = _.str.sprintf(_t("Due in %d days"), Math.abs(diff));
                    }
                }
            }
            activity.label_delay = toDisplay;
        });
        return activities;
    };

    var setFileUploadID = function (activities) {
        _.each(activities, function (activity) {
             activity.fileuploadID = _.uniqueId('o_fileupload');
        });
        return activities;
    };

    Activity.include({
        events: _.extend({}, Activity.prototype.events, {
            'click .o_mark_as_done_attach_upload_file': '_onMarkActivityAttachDoneUploadFile',
            'change input.o_attach_input_file': '_onFileAttachChanged',
        }),
        _render: function () {
            _.each(this._activities, function (activity) {
                var note = mailUtils.parseAndTransform(activity.note || '', mailUtils.inline);
                var is_blank = (/^\s*$/).test(note);
                if (!is_blank) {
                    activity.note = mailUtils.parseAndTransform(activity.note, mailUtils.addLink);
                } else {
                    activity.note = '';
                }
            });
            var activities = setFileUploadID(setDelayLabel(this._activities));
            if (activities.length) {
                var nbActivities = _.countBy(activities, 'state');
                this.$el.html(QWeb.render('mail.activity_items', {
                    uid: session.uid,
                    activities: activities,
                    nbPlannedActivities: nbActivities.planned,
                    nbTodayActivities: nbActivities.today,
                    nbOverdueActivities: nbActivities.overdue,
                    dateFormat: time.getLangDateFormat(),
                    datetimeFormat: time.getLangDatetimeFormat(),
                    session: session,
                    widget: this,
                }));
                this._bindOnUploadAction(this._activities);
            } else {
                this._unbindOnUploadAction(this._activities);
                this.$el.empty();
            }
        },
        _onMarkActivityDone: function (ev) {
            if(!$(ev.target).hasClass("o_attach_input_file")){
                ev.stopPropagation();
                ev.preventDefault();
            }

            var self = this;
            var $markDoneBtn = $(ev.currentTarget);
            var activity = this._activities[0];
//            activity.fileuploadID = _.uniqueId('o_fileupload');
            var activityID = $markDoneBtn.data('activity-id');
            var previousActivityTypeID = $markDoneBtn.data('previous-activity-type-id') || false;
            var forceNextActivity = $markDoneBtn.data('force-next-activity');

            if ($markDoneBtn.data('toggle') == 'collapse') {
                var $actLi = $markDoneBtn.parents('.o_log_activity');
                var $panel = self.$('#o_activity_form_' + activityID);

                if (!$panel.data('bs.collapse')) {
                    var $form = $(QWeb.render('mail.activity_feedback_form', {
                        previous_activity_type_id: previousActivityTypeID,
                        force_next: forceNextActivity
                    }));
                    $panel.append($form);
                    self._onMarkActivityDoneActions($markDoneBtn, $form, activityID);

                    // Close and reset any other open panels
                    _.each($panel.siblings('.o_activity_form'), function (el) {
                        if ($(el).data('bs.collapse')) {
                            $(el).empty().collapse('dispose').removeClass('show');
                        }
                    });

                    // Scroll  to selected activity
                    $markDoneBtn.parents('.o_activity_log_container').scrollTo($actLi.position().top, 100);
                }

                // Empty and reset panel on close
                $panel.on('hidden.bs.collapse', function () {
                    if ($panel.data('bs.collapse')) {
                        $actLi.removeClass('o_activity_selected');
                        $panel.collapse('dispose');
                        $panel.empty();
                    }
                });

                this.$('.o_activity_selected').removeClass('o_activity_selected');
                $actLi.toggleClass('o_activity_selected');
                $panel.collapse('toggle');

            } else if (!$markDoneBtn.data('bs.popover')) {
                $markDoneBtn.popover({
                    template: $(Popover.Default.template).addClass('o_mail_activity_feedback')[0].outerHTML, // Ugly but cannot find another way
                    container: $markDoneBtn,
                    title : _t("Feedback"),
                    html: true,
                    trigger: 'manual',
                    placement: 'right', // FIXME: this should work, maybe a bug in the popper lib
                    content : function () {
                        var $popover = $(QWeb.render('mail.attachment.activity_feedback_form', {
                            previous_activity_type_id: previousActivityTypeID,
                            activity: activity,
                            activityID: activityID,
                            force_next: forceNextActivity
                        }));
                        self._onMarkActivityDoneActions($markDoneBtn, $popover, activityID);
                        return $popover;
                    },
                }).on('shown.bs.popover', function () {
                    var $popover = $($(this).data("bs.popover").tip);
                    $(".o_mail_activity_feedback.popover").not($popover).popover("hide");
                    $popover.addClass('o_mail_activity_feedback').attr('tabindex', 0);
                    $popover.find('#activity_feedback').focus();
                    self._bindPopoverFocusout($(this));
                }).popover('show');
            } else {
                var popover = $markDoneBtn.data('bs.popover');
                if ($('#' + popover.tip.id).length === 0) {
                   popover.show();
                }
            }
        },
        _bindPopoverFocusout: function ($popover_el) {
            var self = this;
            // Retrieve the actual popover's HTML
            var $popover = $($popover_el.data("bs.popover").tip);
            var activityID = $popover_el.data('activity-id');
            $popover.off('focusout');
            $popover.focusout(function (e) {
                // outside click of popover hide the popover
                // e.relatedTarget is the element receiving the focus
                if (!$popover.is(e.relatedTarget) && !$popover.find(e.relatedTarget).length && e.relatedTarget !== null) {
                    self._draftFeedback[activityID] = $popover.find('#activity_feedback').val();
                    self._draftFeedback[activityID+"_attachmentIds"] = $popover.find('#activity_attachment').val();
                    $popover.popover('hide');
                }
            });
        },
        _bindOnUploadAction: function (activities) {
            var self = this;
            _.each(activities, function (activity) {
                if (activity.fileuploadID) {
                    $(window).on(activity.fileuploadID, function() {
                        framework.unblockUI();
                        // find the button clicked and display the feedback popup on it
                        var files = Array.prototype.slice.call(arguments, 1);
                        if (activity.activity_category !== 'upload_file'){
                            var attachmentIds = []
                            var attachmentIdsInput = $(document).find('#activity_attachment');
                            if(attachmentIdsInput.val()){
                                attachmentIds = JSON.parse(attachmentIdsInput.val())
                            }
                            var file_ids = _.pluck(files, 'id')
                            $.each( files, function( key, value ) {
                                var file_id = value.id
                                attachmentIds.push(file_id);


                                if(value.mimetype.match('image.*')){
                                    var preview = '<div class="o_attachment_image" style="border: 1px solid #ccc;border-radius: 5px;background-image:url(/web/image/'+file_id+'/160x160/?crop=true); width: 40px;height: 40px; background-size: contain;  background-repeat: no-repeat;display: inline-block;margin:0 3px; "/>';
                                }else{
                                    var preview = '<div class="o_image o_image_thumbnail" data-mimetype="'+value.mimetype+'"/>';
                                }
                                $(document).find('#attachment_preview').append(preview);
                            });


                            attachmentIdsInput.val(JSON.stringify(attachmentIds));
                            attachmentIdsInput.trigger("change")

                        }else{
                            self._markActivityDone({
                                activityID: activity.id,
                                attachmentIds: _.pluck(files, 'id')
                            }).then(function () {
                                self.trigger_up('reload');
                            });
                        }
                    });
                }
            });
        },
        _onMarkActivityDoneActions: function ($btn, $form, activityID) {
            var self = this;
            var attachments = [];
            $form.find('#activity_feedback').val(self._draftFeedback[activityID]);
            $form.find('#activity_attachment').val(self._draftFeedback[activityID+"_attachmentIds"]);



            $form.on('click', '.o_activity_popover_done', function (ev) {
                ev.stopPropagation();

                var activity_attachments = $form.find('#activity_attachment').val()
                if(activity_attachments){
                    attachments = JSON.parse(activity_attachments);
                }

                self._markActivityDone({
                    activityID: activityID,
                    feedback: _.escape($form.find('#activity_feedback').val()),
                    attachmentIds: attachments,
                });
            });
            $form.on('click', '.o_activity_popover_done_next', function (ev) {
                ev.stopPropagation();

                var activity_attachments = $form.find('#activity_attachment').val()
                if(activity_attachments){
                    attachments = JSON.parse(activity_attachments);
                }

                self._markActivityDoneAndScheduleNext({
                    activityID: activityID,
                    feedback: _.escape($form.find('#activity_feedback').val()),
                    attachmentIds: attachments,
                });
            });
            $form.on('click', '.o_activity_popover_discard', function (ev) {
                ev.stopPropagation();
                if ($btn.data('bs.popover')) {
                    $btn.popover('hide');
                } else if ($btn.data('toggle') == 'collapse') {
                    self.$('#o_activity_form_' + activityID).collapse('hide');
                }
            });
        },

        _onMarkActivityAttachDoneUploadFile: function (ev) {
            ev.preventDefault();
            ev.stopPropagation();
            var fileuploadID = $(ev.currentTarget).data('fileupload-id');
            var $form = this.$("[target='" + fileuploadID + "']");
            var $input = this.$("[target='" + fileuploadID + "'] > input.o_attach_input_file");
            $input.click();
        },
       _onFileAttachChanged: function (ev) {
            ev.stopPropagation();
            ev.preventDefault();
            var $form = $(ev.currentTarget).closest('form');
            $form.submit();
            framework.blockUI();

        },


    });
});