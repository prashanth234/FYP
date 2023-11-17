
SET @user_id = 44;

DELETE FROM `fyp`.`refresh_token_refreshtoken` WHERE (`user_id` = @user_id);
DELETE FROM `fyp`.`graphql_auth_userstatus` WHERE (`user_id` = @user_id);
DELETE FROM `fyp`.`core_coinactivity` WHERE (`user_id` = @user_id);
DELETE FROM `fyp`.`core_user` WHERE (`id` = @user_id);