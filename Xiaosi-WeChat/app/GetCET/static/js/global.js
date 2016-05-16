/**
 * Created by realityone on 15-6-22.
 */
$(document).ready(function () {
        $('form').submit(function () {
            var inputs = Array($(this).find('input[type="text"]'));
            var can_submit = true;
            inputs.forEach(function (e) {
                if (e.val().length == 0) {
                    can_submit = false;
                }
            });
            return can_submit;
        });

        $("#province").change(function () {
            var province = $(this).children('option:selected').val();
            var school = all_school[province];
            var s_set = $('#school');
            s_set.empty();
            school[1].forEach(function (e) {
                s_set.append('<option value=' + e + '>' + e + '</option>');
            });
        });

        $('#getTicket').click(function () {
            var name = $('#tname').val();
            if (name.length <= 0) {
                return false;
            }
            $.ajax({
                url: 'ticket',
                type: 'POST',
                dataType: 'json',
                async: false,
                data: {
                    province: $('#province').val(),
                    school: $('#school').val(),
                    name: name,
                    cet_type: $('input[name="tcet"]:checked').val()
                },
                success: function (data) {
                    var t_number = $('#ticket_number');
                    t_number.empty();
                    if (data['error'] == true) {
                        t_number.append('抱歉，未找到您的准考证');
                    }
                    else {
                        t_number.append('您的准考证为: <span>' +data['ticket_number'] + '</span>');
                    }
                }
            })
        });
    }
);