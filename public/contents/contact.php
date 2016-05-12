<!-- BEGIN CONTACT -->

<section id="contact" class="contact-section">

    <div class="container">

        <h3><?= $registerHeadline; ?></h3>
        <h5 class="center"><?= $registerSubHeadline; ?></h5>

        <form name="ProfileForm" onsubmit="return CheckInputs();" action="https://news.t-systems-mms.com/u/register.php" method=get class="contact-form">
            <input type=hidden name="CID" value="112554395">
            <input type=hidden name="SID" value="<?= $SID; ?>">
            <input type=hidden name="UID" value="<?= $UID; ?>">
            <input type=hidden name="f" value="36664"><input type=hidden name="p" value="2">
            <input type=hidden name="a" value="r">
            <input type=hidden name="el" value="<?= $el; ?>">
            <input type=hidden name="endlink" value="<?= $endlink; ?>">
            <input type=hidden name="llid" value="<?= $llid; ?>">
            <input type=hidden name="c" value="<?= $c; ?>">
            <input type=hidden name="counted" value="<?= $counted; ?>">
            <input type=hidden name="RID" value="<?= $RID; ?>">
            <input type=hidden name="mailnow" value="<?= $mailnow; ?>">
            <div class="main-form">

                <div class="row">

                    <div class="col-lg-4 col-md-4 col-sm-4 col-xs-12">

                        <label>
                            <select name="inp_46" size="1" required>
                                <option value=""> </option>
                                <option value="1"<?= ($inp_46 == "Herr") ? " SELECTED" : ""; ?>>Herr</option>
                                <option value="2"<?= ($inp_46 == "Frau") ? " SELECTED" : ""; ?>>Frau</option>
                            </select>
                            <i>
                                <svg role="img" fill="currentColor">
                                    <use xlink:href="svgicons/icons.svg#name-icon"></use>
                                </svg>
                            </i>
                            <span class="uppercase"><?= $registerAnrede; ?></span>
                        </label>
                    </div>

                    <div class="col-lg-4 col-md-4 col-sm-4 col-xs-12">
                        <label>
                            <input class="gray" type="text" name="inp_1" maxlength="60" value="<?= $inp_1; ?>" required>
                            <i>
                                <svg role="img" fill="currentColor">
                                    <use xlink:href="svgicons/icons.svg#name-icon"></use>
                                </svg>
                            </i>
                            <span class="uppercase"><?= $registerFirstName; ?></span>
                        </label>

                    </div>

                    <div class="col-lg-4 col-md-4 col-sm-4 col-xs-12">
                        <label>
                            <input class="gray" type="text" name="inp_2" maxlength="60" value="<?= $inp_2; ?>" required>
                            <i>
                                <svg role="img" fill="currentColor">
                                    <use xlink:href="svgicons/icons.svg#name-icon"></use>
                                </svg>
                            </i>
                            <span class="uppercase"><?= $registerName; ?></span>
                        </label>

                    </div>

                </div>

                <div class="row">
                    <div class="col-lg-4 col-md-4 col-sm-4 col-xs-12">
                        <label>
                            <input class="gray" type="text" name="inp_3" maxlength="255" value="<?= $inp_3; ?>" required>
                            <i>
                                <svg role="img" fill="currentColor">
                                    <use xlink:href="svgicons/icons.svg#mail-icon"></use>
                                </svg>
                            </i>
                            <span class="uppercase"><?= $registerMail; ?></span>
                    </label>

                </div>
                <div class="col-lg-4 col-md-4 col-sm-4 col-xs-12">
                    <label>
                        <input class="gray" type="text" maxlength="255" name="inp_56723" value="<?= $inp_56723; ?>">
                        <i>
                            <svg role="img" fill="currentColor">
                                <use xlink:href="svgicons/icons.svg#text-icon"></use>
                            </svg>
                        </i>
                        <span class="uppercase"><?= $registerCompany; ?></span>
                        </label>

                    </div>

                    <div class="col-lg-4 col-md-4 col-sm-4 col-xs-12">
                        <label>
                            <input class="gray" type="text" maxlength="255" name="inp_56722" value="<?= $inp_56722; ?>">
                            <i>
                                <svg role="img" fill="currentColor">
                                    <use xlink:href="svgicons/icons.svg#text-icon"></use>
                                </svg>
                            </i>
                            <span class="uppercase"><?= $registerPosition; ?></span>
                        </label>

                    </div>
                </div>

                <div class="row">

                    <div class="col-lg-12">
                        <label>
                            <input type="text" maxlength="255" name="inp_56724" value="<?= $inp_56724; ?>">
                            <i>
                                <svg role="img" fill="currentColor">
                                    <use xlink:href="svgicons/icons.svg#text-icon"></use>
                                </svg>
                            </i>
                            <span><?= $registerOptional; ?></span>
                        </label>

                    </div>

                </div>

            </div>



            <button class="btn1 btn--white big right" onclick="javascript:SubmitIt()">
                <?= $registerSubmit; ?>
                <span>
                    <svg role="img" fill="currentColor">
                        <use xlink:href="svgicons/icons.svg#arrow-down"></use>
                    </svg>
                </span>
            </button>
            <div class="clearfix"></div>
        </div>

        <?php include 'register_scripts.php' ?>
    </form>

</div>

</section>

                <!-- END CONTACT -->
<?php
// vim: et sw=2 ts=2 ai si
?>
