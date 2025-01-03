
SET @user_id = '14';

DELETE FROM `fyp`.`refresh_token_refreshtoken` WHERE (`user_id` = @user_id);
DELETE FROM `fyp`.`authentication_userstatus` WHERE (`user_id` = @user_id);
DELETE FROM `fyp`.`core_coinactivity` WHERE (`user_id` = @user_id);
DELETE FROM `fyp`.`categories_like` WHERE (`user_id` = @user_id);
DELETE FROM `fyp`.`core_support` WHERE (`user_id` = @user_id);
DELETE FROM `fyp`.`categories_winner` WHERE (`user_id` = @user_id);
DELETE FROM `fyp`.`categories_postfile` WHERE (`post_id` in (SELECT id FROM fyp.categories_post where `user_id`= @user_id));
DELETE FROM `fyp`.`categories_post` WHERE (`user_id` = @user_id);
DELETE FROM `fyp`.`core_user` WHERE (`id` = @user_id);

